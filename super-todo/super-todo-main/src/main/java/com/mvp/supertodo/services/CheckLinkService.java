package com.mvp.supertodo.services;

import com.mvp.supertodo.dto.*;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import java.io.*;
import java.util.Arrays;
import java.util.List;

@Slf4j
@Service
public class CheckLinkService {

    private String scriptName = "/tmp/checker.sh";

    public StatusResponse checkLink(String link) {
        ProcessBuilder processBuilder = null;
        Process process = null;
        createScript(link);
        List<String> parsedCommand = getCommandsList();
        try {
            processBuilder = new ProcessBuilder(parsedCommand);
            process = processBuilder.start();
            try (
                InputStreamReader inputStreamReader = new InputStreamReader(process.getInputStream());
                BufferedReader bufferedReader = new BufferedReader(inputStreamReader);
            ) {
                String output = null;
                Boolean result = null;
                while ((output = bufferedReader.readLine()) != null) {
                    System.out.println(output);
                    result = parseRequest(output);
                    if (result) {
                        return new StatusResponse(true);
                    }

                }
            }
            process.waitFor();
            process.destroy();
        } catch (IOException | InterruptedException err) {
            log.error(err.getMessage(), err);
        }
        return new StatusResponse(false);
    }

    private List<String> getCommandsList() {
        var command = "sh " + scriptName;
        List<String> parsedCommandList = Arrays
            .stream(
                command
                    .split(" ")
            ).toList();
        return parsedCommandList;
    }

    private Boolean parseRequest(String request) {
        if (request.startsWith("HTTP")) {
            String[] parseString = request.split(" ");
            Integer statusCode = Integer.parseInt(parseString[1]);
            if (statusCode < 400) {
                return true;
            }
        }
        return false;
    }

    private void createScript(String link) {
        File file = new File(scriptName);
        createFile(file);
        try {
            FileWriter fileWriter = new FileWriter(scriptName);
            fileWriter.write("#!/usr/bin/sh\n");
            fileWriter.write("curl -Is " + link);
            fileWriter.close();
        } catch (IOException err) {
            log.error(err.getMessage(), err);
        }
    }

    private void createFile(File file) {
        if (isExistScript(file)) {
            file.delete();
        }
        try {
            file.createNewFile();
        } catch (IOException e) {
            log.error(e.getMessage(), e);
        }
    }

    private Boolean isExistScript(File file) {
        return file.exists();
    }
}

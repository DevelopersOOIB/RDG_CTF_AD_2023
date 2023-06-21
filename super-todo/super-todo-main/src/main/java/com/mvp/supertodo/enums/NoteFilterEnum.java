package com.mvp.supertodo.enums;

public enum NoteFilterEnum {
    ALL("All"),
    ACTIVE("Active"),
    COMPLETED("Completed");

    private final String value;

    private  NoteFilterEnum(String value) {
        this.value = value;
    }

    public String getValue() {
        return value;
    }

}

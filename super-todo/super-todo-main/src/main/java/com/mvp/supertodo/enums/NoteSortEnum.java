package com.mvp.supertodo.enums;

public enum NoteSortEnum {
    TIMESTAMP("Added date"),
    COMPLETED_AT("Completion date");

    private String value;

    private  NoteSortEnum(String value) {
        this.value = value;
    }

    public String getValue() {
        return value;
    }
}

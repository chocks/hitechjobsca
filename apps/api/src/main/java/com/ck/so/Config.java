package com.ck.so;

import org.apache.commons.io.FileUtils;

import java.io.File;
import java.util.List;

public class Config {
    private static final String configFile = "/etc/opt/jobs-download/.config";
    private static String dbUserName;
    private static String dbPassword;
    private static String dbHost;
    private static String dbName;

    public static void init() {
        try {
            File f = new File(configFile);
            List<String> lines = FileUtils.readLines(f, "UTF-8");

            for (String line : lines) {
                String[] properties = line.split("=");
                switch (properties[0]) {
                    case "DB_HOST":
                        setDbHost(properties[1].trim());
                        break;
                    case "DB_NAME":
                        setDbName(properties[1].trim());
                        break;
                    case "DB_USER":
                        setDbUserName(properties[1].trim());
                        break;
                    case "DB_PASSWORD":
                        setDbPassword(properties[1].trim());
                        break;
                }
            }
        } catch (Exception exp) {
            exp.printStackTrace();
        }

    }

    public static String getDbUserName() {
        return dbUserName;
    }

    public static void setDbUserName(String dbUserName) {
        Config.dbUserName = dbUserName;
    }

    public static String getDbPassword() {
        return dbPassword;
    }

    public static void setDbPassword(String dbPassword) {
        Config.dbPassword = dbPassword;
    }

    public static String getDbHost() {
        return dbHost;
    }

    public static void setDbHost(String dbHost) {
        Config.dbHost = dbHost;
    }

    public static String getDbName() {
        return dbName;
    }

    public static void setDbName(String dbName) {
        Config.dbName = dbName;
    }
}

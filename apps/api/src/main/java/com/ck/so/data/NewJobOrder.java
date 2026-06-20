package com.ck.so.data;


public class NewJobOrder {
    private String title;
    private String companyName;
    private String applyUrl;
    private String salaryRange;
    private String location;
    private String contact;

    protected NewJobOrder() {}

    public NewJobOrder(String title, String companyName, String applyUrl, String salaryRange, String location, String contact) {
        this.title = title;
        this.companyName = companyName;
        this.applyUrl = applyUrl;
        this.salaryRange = salaryRange;
        this.location = location;
        this.contact = contact;
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public String getCompanyName() {
        return companyName;
    }

    public void setCompanyName(String companyName) {
        this.companyName = companyName;
    }

    public String getApplyUrl() {
        return applyUrl;
    }

    public void setApplyUrl(String applyUrl) {
        this.applyUrl = applyUrl;
    }

    public String getSalaryRange() {
        return salaryRange;
    }

    public void setSalaryRange(String salaryRange) {
        this.salaryRange = salaryRange;
    }

    public String getLocation() {
        return location;
    }

    public void setLocation(String location) {
        this.location = location;
    }

    public String getContact() {
        return contact;
    }

    public void setContact(String contact) {
        this.contact = contact;
    }
}

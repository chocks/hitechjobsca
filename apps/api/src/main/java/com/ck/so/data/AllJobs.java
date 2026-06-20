package com.ck.so.data;

import jakarta.persistence.*;
import java.sql.Date;
import java.time.LocalDate;
import java.util.UUID;

@Entity
@Table(schema = "jobs")
public class AllJobs {
    @Id
    @GeneratedValue(strategy=GenerationType.IDENTITY)
    private Long id;
    private String title;
    private String companyName;
    private String applyUrl;
    private String salaryRange;
    @Column(columnDefinition = "varchar(64)")
    private String location = "Canada";
    @Column(columnDefinition = "date")
    private Date fromDate = Date.valueOf(LocalDate.now());
    @Column(columnDefinition = "date")
    private Date endDate = Date.valueOf(LocalDate.now().plusDays(60));
    @Transient
    private String searchVectors;
    private Integer rank;
    private Boolean status;
    private Boolean pinned;
    private String ext_id;

    protected AllJobs() {}

    public AllJobs(String title, String companyName, String applyUrl,
                   String salaryRange, String location) {
        this.title = title;
        this.companyName = companyName;
        this.applyUrl = applyUrl;
        this.salaryRange = salaryRange;
        this.location = location;
        this.rank = 10;
        this.status = true;
        this.pinned = false;
        this.ext_id = UUID.randomUUID().toString();
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

    public Date getFromDate() {
        return fromDate;
    }

    public void setFromDate(Date fromDate) {
        this.fromDate = fromDate;
    }

    public Date getEndDate() {
        return endDate;
    }

    public void setEndDate(Date endDate) {
        this.endDate = endDate;
    }

    public Long getId() {
        return id;
    }

    public Integer getRank() {
        return rank;
    }

    public void setRank(Integer rank) {
        this.rank = rank;
    }

    public Boolean getStatus() {
        return status;
    }

    public void setStatus(Boolean status) {
        this.status = status;
    }

    public Boolean getPinned() {
        return pinned;
    }

    public void setPinned(Boolean pinned) {
        this.pinned = pinned;
    }
}

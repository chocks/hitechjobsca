package com.ck.so.data;

import javax.persistence.*;
import java.sql.Date;
import java.time.LocalDate;

@Entity
@Table(schema = "jobs")
public class Orders {
    @Id
    @GeneratedValue(strategy= GenerationType.AUTO)
    private Long id;
    private String token;
    private boolean status;
    private String contact;
    private Integer amount;
    private String currency;
    @Column(columnDefinition = "date default now()")
    private Date date = Date.valueOf(LocalDate.now());
    private String description;

    protected Orders() {}

    public Orders(String token, boolean status, String contact,
                  Integer amount, String currency) {
        this.token = token;
        this.status = status;
        this.contact = contact;
        this.amount = amount;
        this.currency = currency;
    }

    public Orders(String contact, String description) {
        this.token = "blahabhabdifu121";
        this.status = true;
        this.contact = contact;
        this.amount = 250;
        this.currency = "cad";
        this.description = description;
    }

    public String getToken() {
        return token;
    }

    public void setToken(String token) {
        this.token = token;
    }

    public boolean isStatus() {
        return status;
    }

    public void setStatus(boolean status) {
        this.status = status;
    }

    public String getContact() {
        return contact;
    }

    public void setContact(String contact) {
        this.contact = contact;
    }

    public Integer getAmount() {
        return amount;
    }

    public void setAmount(Integer amount) {
        this.amount = amount;
    }

    public String getCurrency() {
        return currency;
    }

    public void setCurrency(String currency) {
        this.currency = currency;
    }

    public Date getDate() {
        return date;
    }

    public void setDate(Date date) {
        this.date = date;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public Long getId() {
        return id;
    }
}

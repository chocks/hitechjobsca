package com.ck.so.data;


import javax.persistence.*;

@Entity
@Table(schema = "jobs")
public class OrderJob {
    @Id
    @GeneratedValue(strategy= GenerationType.AUTO)
    private Long id;
    private Long jobId;
    private Long orderId;

    protected OrderJob() {}

    public OrderJob(Long jobId, Long orderId) {
        this.jobId = jobId;
        this.orderId = orderId;
    }

    public Long getJobId() {
        return jobId;
    }

    public void setJobId(Long jobId) {
        this.jobId = jobId;
    }

    public Long getOrderId() {
        return orderId;
    }

    public void setOrderId(Long orderId) {
        this.orderId = orderId;
    }

    @Override
    public String toString() {
        return "OrderJob{" +
                "jobId=" + jobId +
                ", orderId=" + orderId +
                '}';
    }
}

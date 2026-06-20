package com.ck.so.resource;


import com.ck.so.data.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;

@Service
public class JobsResource {

    private List<AllJobs> allJobs;

    public JobsResource() {}

    public JobsResource(AllJobsRepository jobsRepository) {
        this.allJobs = jobsRepository.findAllActiveJobs();
    }


    public JobsResource(NewJobOrder newJobOrder,
                        AllJobsRepository jobsRepository,
                        OrderInterface orderRepository,
                        OrderJobInterface orderJobRepository){
        this.allJobs = new ArrayList<>();
        AllJobs newJob = new AllJobs(newJobOrder.getTitle(), newJobOrder.getCompanyName(), newJobOrder.getApplyUrl(),
                newJobOrder.getSalaryRange(), newJobOrder.getLocation());
        newJob = jobsRepository.save(newJob);
        Orders newOrder = new Orders(newJobOrder.getContact(), "Created via api");
        newOrder = orderRepository.save(newOrder);
        this.allJobs.add(newJob);
        orderJobRepository.save(new OrderJob(newJob.getId(), newOrder.getId()));
    }

    public List<AllJobs> getAllJobs() {
        return allJobs;
    }

    public JobsResource(String searchString, AllJobsRepository jobsRepository) {
        this.allJobs = jobsRepository.findMatchingJobs(searchString);
    }

}

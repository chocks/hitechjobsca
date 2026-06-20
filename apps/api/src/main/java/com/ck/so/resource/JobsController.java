package com.ck.so.resource;

import com.ck.so.data.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

@RestController
public class JobsController {
    @Autowired
    AllJobsRepository jobsRepository;

    @Autowired
    OrderInterface orderRepository;

    @Autowired
    OrderJobInterface orderJobRepository;


    @CrossOrigin()
    @RequestMapping("/ca_jobs")
    public JobsResource caJobs() {
        return new JobsResource(jobsRepository);
    }

    @CrossOrigin()
    @RequestMapping(path="/new", method= RequestMethod.POST)
    public JobsResource createJob(@RequestBody NewJobOrder newJobOrder) throws Exception {
        return new JobsResource(newJobOrder, jobsRepository, orderRepository, orderJobRepository);
    }

    @CrossOrigin()
    @RequestMapping(path="/search")
    public JobsResource searchJobs(@RequestParam String searchString) throws Exception {
        return new JobsResource(searchString, jobsRepository);
    }
}

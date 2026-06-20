package com.ck.so.data;

import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;
import org.springframework.data.repository.CrudRepository;

import java.util.List;


@Repository
public interface AllJobsRepository extends CrudRepository<AllJobs, Long> {
    @Query("select a from AllJobs a where a.endDate >= now() AND " +
            "a.status is True ORDER BY a.rank ASC, a.fromDate DESC")
    List<AllJobs> findAllActiveJobs();

    @Query(value = "SELECT aj.* FROM jobs.all_jobs as aj " +
            "WHERE aj.search_vectors @@ plainto_tsquery(:searchString) " +
            "AND aj.status is True " +
            "ORDER BY aj.rank ASC, aj.from_date DESC", nativeQuery = true)
    List<AllJobs> findMatchingJobs(@Param("searchString") String searchString);
}

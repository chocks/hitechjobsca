package com.ck.so.data;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface OrderInterface extends CrudRepository<Orders, Long> {
}

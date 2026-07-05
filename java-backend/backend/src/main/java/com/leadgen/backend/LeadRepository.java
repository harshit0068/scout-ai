package com.leadgen.backend;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;

public interface LeadRepository extends JpaRepository<Lead, Long> {
    List<Lead> findByIsGenuineOrderByConfidenceScoreDesc(Integer isGenuine);
}
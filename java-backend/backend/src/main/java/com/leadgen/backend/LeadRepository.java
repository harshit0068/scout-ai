package com.leadgen.backend;

import org.springframework.data.jpa.repository.JpaRepository;

public interface LeadRepository extends JpaRepository<Lead, Long> {
    // That's it for now! JpaRepository automatically gives us
    // methods like findAll(), findById(), save(), delete() for free.
}
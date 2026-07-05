package com.leadgen.backend;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/leads")
public class LeadController {

    @Autowired
    private LeadRepository leadRepository;

    @GetMapping
    public List<Lead> getGenuineLeads() {
        return leadRepository.findByIsGenuineOrderByConfidenceScoreDesc(1);
    }

    @GetMapping("/stats")
    public List<Map<String, Object>> getSourceStats() {
        List<Lead> all = leadRepository.findAll();

        Map<String, List<Lead>> bySource = all.stream()
                .filter(l -> l.getSource() != null)
                .collect(Collectors.groupingBy(Lead::getSource));

        List<Map<String, Object>> stats = new ArrayList<>();
        for (Map.Entry<String, List<Lead>> entry : bySource.entrySet()) {
            long total = entry.getValue().size();
            long genuine = entry.getValue().stream()
                    .filter(l -> l.getIsGenuine() != null && l.getIsGenuine() == 1)
                    .count();

            Map<String, Object> row = new HashMap<>();
            row.put("source", entry.getKey());
            row.put("total", total);
            row.put("genuine", genuine);
            row.put("rate", total == 0 ? 0 : Math.round((genuine * 1000.0 / total)) / 10.0);
            stats.add(row);
        }
        return stats;
    }
}
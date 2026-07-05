package com.leadgen.backend;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

@Entity
@Table(name = "leads")
public class Lead {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String source;
    private String author;
    private String url;
    private String text;

    @Column(name = "is_genuine")
    private Integer isGenuine;

    @Column(name = "confidence_score")
    private Double confidenceScore;

    private String summary;

    @Column(name = "created_at")
    private String createdAt;

    public Long getId() { return id; }
    public String getSource() { return source; }
    public String getAuthor() { return author; }
    public String getUrl() { return url; }
    public String getText() { return text; }
    public Integer getIsGenuine() { return isGenuine; }
    public Double getConfidenceScore() { return confidenceScore; }
    public String getSummary() { return summary; }
    public String getCreatedAt() { return createdAt; }
}
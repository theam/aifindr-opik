package com.comet.opik.infrastructure;

import com.fasterxml.jackson.annotation.JsonProperty;

import jakarta.validation.constraints.NotEmpty;
import lombok.Data;

@Data
public class ExperimentRunnerConfig {
    
    @NotEmpty
    @JsonProperty()
    private String url;
} 
package com.ywt.sms.controller;

import com.ywt.sms.common.ApiResponse;
import com.ywt.sms.common.PageResult;
import com.ywt.sms.mapper.ScoreMapper;
import com.ywt.sms.model.Score;
import com.ywt.sms.model.ScoreView;
import jakarta.validation.Valid;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/scores")
public class ScoreController {
    private final ScoreMapper scoreMapper;

    public ScoreController(ScoreMapper scoreMapper) {
        this.scoreMapper = scoreMapper;
    }

    @GetMapping
    public ApiResponse<PageResult<ScoreView>> page(@RequestParam(defaultValue = "") String keyword,
                                                   @RequestParam(defaultValue = "1") int page,
                                                   @RequestParam(defaultValue = "10") int size) {
        int offset = Math.max(page - 1, 0) * size;
        return ApiResponse.ok(new PageResult<>(scoreMapper.findPage(keyword, size, offset), scoreMapper.count(keyword)));
    }

    @PostMapping
    public ApiResponse<Score> create(@Valid @RequestBody Score score) {
        scoreMapper.insert(score);
        return ApiResponse.ok(score);
    }

    @PutMapping("/{id}")
    public ApiResponse<Score> update(@PathVariable Long id, @Valid @RequestBody Score score) {
        score.setId(id);
        scoreMapper.update(score);
        return ApiResponse.ok(score);
    }

    @DeleteMapping("/{id}")
    public ApiResponse<Void> delete(@PathVariable Long id) {
        scoreMapper.delete(id);
        return ApiResponse.ok(null);
    }
}


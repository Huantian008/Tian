package com.ywt.sms;

import com.ywt.sms.common.ApiResponse;
import org.junit.jupiter.api.Test;

import static org.assertj.core.api.Assertions.assertThat;

class ApiResponseTests {
    @Test
    void okResponseCarriesData() {
        ApiResponse<String> response = ApiResponse.ok("ready");

        assertThat(response.isSuccess()).isTrue();
        assertThat(response.getData()).isEqualTo("ready");
        assertThat(response.getMessage()).isEqualTo("操作成功");
    }
}


package com.example.homework5;

import java.util.Arrays;

import org.aspectj.lang.JoinPoint;
import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.After;
import org.aspectj.lang.annotation.AfterReturning;
import org.aspectj.lang.annotation.AfterThrowing;
import org.aspectj.lang.annotation.Around;
import org.aspectj.lang.annotation.Aspect;
import org.aspectj.lang.annotation.Before;
import org.springframework.stereotype.Component;

@Aspect
@Component
public class StudentServiceAspect {
    @Before("studentServiceMethods()")
    public void beforeMethod(JoinPoint joinPoint) {
        System.out.println("[Before] 即将执行方法: " + joinPoint.getSignature().getName()
                + ", 参数: " + Arrays.toString(joinPoint.getArgs()));
    }

    @AfterReturning(pointcut = "studentServiceMethods()", returning = "result")
    public void afterReturningMethod(JoinPoint joinPoint, Object result) {
        System.out.println("[AfterReturning] 方法执行成功: " + joinPoint.getSignature().getName()
                + ", 返回值: " + result);
    }

    @AfterThrowing(pointcut = "studentServiceMethods()", throwing = "exception")
    public void afterThrowingMethod(JoinPoint joinPoint, Exception exception) {
        System.out.println("[AfterThrowing] 方法执行异常: " + joinPoint.getSignature().getName()
                + ", 异常信息: " + exception.getMessage());
    }

    @After("studentServiceMethods()")
    public void afterMethod(JoinPoint joinPoint) {
        System.out.println("[After] 方法执行结束: " + joinPoint.getSignature().getName());
    }

    @Around("execution(* com.example.homework5.StudentService.deleteStudent(..))")
    public Object aroundDeleteStudent(ProceedingJoinPoint proceedingJoinPoint) throws Throwable {
        Object[] args = proceedingJoinPoint.getArgs();
        if (args.length == 0 || !(args[0] instanceof String studentId) || studentId.trim().isEmpty()) {
            System.out.println("[Around] 权限/参数校验失败: 学号不能为空，禁止删除");
            throw new IllegalArgumentException("删除学生时学号不能为空");
        }

        System.out.println("[Around] 权限/参数校验通过，可以删除学号: " + studentId);
        Object result = proceedingJoinPoint.proceed();
        System.out.println("[Around] 删除方法执行完成");
        return result;
    }

    @org.aspectj.lang.annotation.Pointcut("execution(* com.example.homework5.StudentService.*(..))")
    public void studentServiceMethods() {
    }
}

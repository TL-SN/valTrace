#include <stdio.h>
#include <stdlib.h>
#include <math.h>

// 第一层函数声明
int calculate_factorial(int n);
double calculate_power(double base, int exponent);
void process_data(int input);
void display_results(int result1, double result2, int result3);

// 第二层函数声明  
int recursive_multiply(int a, int b);
double calculate_square_root(double x);
int validate_input(int value);

// 第三层函数声明
int check_prime(int num);
double advanced_calculation(double a, double b);

// 主函数 - 程序入口
int main(int argc, char *argv[]) {
    // 检查是否提供了输入参数
    if (argc != 2) {
        printf("错误：请提供一个整数参数。\n");
        return 1; // 错误退出
    }

    // 将命令行参数转换为整数
    int input_value = atoi(argv[1]);

    // 检查输入值是否有效
    if (input_value <= 0) {
        printf("错误：输入的值必须为正整数。\n");
        return 1; // 错误退出
    }

    printf("程序开始执行...\n");
    printf("输入值: %d\n", input_value);
    
    // 调用第一层函数
    process_data(input_value);
    
    printf("程序执行完成。\n");
    return 0;
}

// 第一层函数实现
int calculate_factorial(int n) {
    printf("计算阶乘: %d\n", n);
    if (n <= 1) {
        return 1;
    }
    
    // 嵌套调用：递归计算阶乘
    return n * calculate_factorial(n - 1);
}

double calculate_power(double base, int exponent) {
    printf("计算幂: %.2f^%d\n", base, exponent);
    
    if (exponent == 0) {
        return 1.0;
    }
    
    double result = base;
    for (int i = 1; i < exponent; i++) {
        result *= base;
    }
    
    // 嵌套调用：验证结果
    if (validate_input((int)result)) {
        printf("幂计算结果验证通过\n");
    }
    
    return result;
}

void process_data(int input) {
    printf("\n=== 处理数据 ===\n");
    getchar(); // 用于调试时暂停输出，方便观察
    // 嵌套调用多个第二层函数
    int fact_result = calculate_factorial(input);
    double power_result = calculate_power(2.5, input);
    int multiply_result = recursive_multiply(input, 3);
    
    // 嵌套调用第三层函数
    double advanced_result = advanced_calculation(fact_result, power_result);
    
    printf("高级计算结果: %.2f\n", advanced_result);
    
    // 显示所有结果
    display_results(fact_result, power_result, multiply_result);
}

// 第二层函数实现
int recursive_multiply(int a, int b) {
    printf("递归乘法: %d * %d\n", a, b);
    
    if (b == 0) {
        return 0;
    }
    if (b == 1) {
        return a;
    }
    
    // 嵌套调用：递归乘法
    return a + recursive_multiply(a, b - 1);
}

double calculate_square_root(double x) {
    printf("计算平方根: %.2f\n", x);
    
    if (x < 0) {
        printf("错误：不能计算负数的平方根\n");
        return -1;
    }
    
    // 使用数学库函数
    double result = sqrt(x);
    
    // 嵌套调用：验证结果
    if (validate_input((int)result)) {
        printf("平方根计算完成\n");
    }
    
    return result;
}

int validate_input(int value) {
    printf("验证输入值: %d\n", value);
    
    if (value < 0) {
        printf("警告：值为负数\n");
        return 0;
    }
    
    if (value > 1000) {
        printf("警告：值过大\n");
        return 0;
    }
    
    // 嵌套调用：检查是否为质数
    if (check_prime(value)) {
        printf("值 %d 是质数\n", value);
    } else {
        printf("值 %d 不是质数\n", value);
    }
    
    return 1;
}

// 第三层函数实现
int check_prime(int num) {
    printf("检查质数: %d\n", num);
    
    if (num <= 1) {
        return 0;
    }
    if (num <= 3) {
        return 1;
    }
    if (num % 2 == 0 || num % 3 == 0) {
        return 0;
    }
    
    // 检查6k±1形式的因数
    for (int i = 5; i * i <= num; i += 6) {
        if (num % i == 0 || num % (i + 2) == 0) {
            return 0;
        }
    }
    
    return 1;
}

double advanced_calculation(double a, double b) {
    printf("执行高级计算: %.2f 和 %.2f\n", a, b);
    
    // 嵌套调用多个函数
    double sqrt_a = calculate_square_root(a);
    double power_b = calculate_power(b, 2);
    
    if (sqrt_a < 0) {
        sqrt_a = 1.0; // 默认值
    }
    
    double result = (sqrt_a + power_b) / 2.0;
    
    printf("高级计算完成，结果: %.2f\n", result);
    return result;
}

void display_results(int result1, double result2, int result3) {
    printf("\n=== 结果显示 ===\n");
    printf("阶乘结果: %d\n", result1);
    printf("幂计算结果: %.2f\n", result2);
    printf("乘法结果: %d\n", result3);
    
    // 嵌套调用：计算并显示平方根
    double sqrt_result = calculate_square_root(result2);
    if (sqrt_result >= 0) {
        printf("结果的平方根: %.2f\n", sqrt_result);
    }
}

import pytest
import time
from app import app

# 尝试导入allure，如果不可用则跳过
try:
    import allure
    ALLURE_AVAILABLE = True
except ImportError:
    allure = None
    ALLURE_AVAILABLE = False

class TestHelloWorldService:
    
    @classmethod
    def setup_class(cls):
        """设置测试客户端"""
        cls.client = app.test_client()
    
    def test_health_check(self):
        """Test health check endpoint"""
        if ALLURE_AVAILABLE:
            with allure.step("Send GET request to /health"):
                response = self.__class__.client.get('/health')
            
            with allure.step("Verify response status code"):
                assert response.status_code == 200
            
            with allure.step("Verify response content"):
                data = response.get_json()
                assert data["status"] == "healthy"
                assert data["service"] == "hello-world-service"
        else:
            response = self.__class__.client.get('/health')
            assert response.status_code == 200
            data = response.get_json()
            assert data["status"] == "healthy"
            assert data["service"] == "hello-world-service"
    
    def test_hello_world(self):
        """Test hello world endpoint"""
        if ALLURE_AVAILABLE:
            with allure.step("Send GET request to /hello"):
                response = self.__class__.client.get('/hello')
            
            with allure.step("Verify response status code"):
                assert response.status_code == 200
            
            with allure.step("Verify response content"):
                data = response.get_json()
                assert data["message"] == "Hello World"
                assert data["status"] == "success"
                assert data["version"] == "1.0.0"
        else:
            response = self.__class__.client.get('/hello')
            assert response.status_code == 200
            data = response.get_json()
            assert data["message"] == "Hello World"
            assert data["status"] == "success"
            assert data["version"] == "1.0.0"
    
    def test_response_time(self):
        """Test response time is within acceptable limits"""
        if ALLURE_AVAILABLE:
            with allure.step("Measure response time for /hello"):
                start_time = time.time()
                response = self.__class__.client.get('/hello')
                end_time = time.time()
            
            with allure.step("Verify response time is under 3 seconds"):
                response_time = end_time - start_time
                assert response_time < 3.0, f"Response time {response_time}s exceeds 3s limit"
        else:
            start_time = time.time()
            response = self.__class__.client.get('/hello')
            end_time = time.time()
            
            response_time = end_time - start_time
            assert response_time < 3.0, f"Response time {response_time}s exceeds 3s limit"
    
    def test_invalid_endpoint(self):
        """Test handling of invalid endpoints"""
        if ALLURE_AVAILABLE:
            with allure.step("Send GET request to non-existent endpoint"):
                response = self.__class__.client.get('/nonexistent')
            
            with allure.step("Verify 404 status code"):
                assert response.status_code == 404
        else:
            response = self.__class__.client.get('/nonexistent')
            assert response.status_code == 404
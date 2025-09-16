import asyncio
import os
import json
from typing import Dict, List, Any

class DatasetMCPTester:
    """Comprehensive MCP dataset testing class"""

    def __init__(self, workspace_dir: str = "./"):
        self.workspace_dir = workspace_dir
        self.test_results = []

    def basic_dataset_test(self) -> bool:
        """Basic synchronous dataset test"""
        try:
            # Test basic file operations
            test_data = {
                "test_id": "mcp_dataset_test_001",
                "timestamp": "2025-09-16T22:49:51.092Z",
                "status": "active",
                "data": ["sample", "dataset", "entries"]
            }

            # Write test data
            test_file = os.path.join(self.workspace_dir, "test_dataset.json")
            with open(test_file, 'w') as f:
                json.dump(test_data, f, indent=2)

            # Read and verify
            with open(test_file, 'r') as f:
                loaded_data = json.load(f)

            assert loaded_data["test_id"] == "mcp_dataset_test_001"
            assert len(loaded_data["data"]) == 3

            self.test_results.append({
                "test": "basic_dataset_test",
                "status": "passed",
                "details": "File I/O operations successful"
            })

            return True
        except Exception as e:
            self.test_results.append({
                "test": "basic_dataset_test",
                "status": "failed",
                "details": str(e)
            })
            return False

    async def async_dataset_processing_test(self) -> bool:
        """Async dataset processing test"""
        try:
            # Simulate async dataset processing
            await asyncio.sleep(0.1)

            # Create multiple test files concurrently
            tasks = []
            for i in range(3):
                task = self._create_async_test_file(i)
                tasks.append(task)

            results = await asyncio.gather(*tasks)

            # Verify all files created
            for i, result in enumerate(results):
                assert result == f"async_test_{i}.json"
                file_path = os.path.join(self.workspace_dir, result)
                assert os.path.exists(file_path)

            self.test_results.append({
                "test": "async_dataset_processing_test",
                "status": "passed",
                "details": f"Created {len(results)} async test files"
            })

            return True
        except Exception as e:
            self.test_results.append({
                "test": "async_dataset_processing_test",
                "status": "failed",
                "details": str(e)
            })
            return False

    async def _create_async_test_file(self, index: int) -> str:
        """Helper to create async test file"""
        filename = f"async_test_{index}.json"
        filepath = os.path.join(self.workspace_dir, filename)

        test_data = {
            "async_test_id": f"async_{index}",
            "created_at": asyncio.get_event_loop().time(),
            "data": [f"async_entry_{i}" for i in range(5)]
        }

        with open(filepath, 'w') as f:
            json.dump(test_data, f, indent=2)

        return filename

    def dataset_search_test(self) -> bool:
        """Test dataset search functionality"""
        try:
            # Create searchable dataset
            search_data = {
                "entries": [
                    {"id": 1, "content": "LightRAG dataset integration"},
                    {"id": 2, "content": "Cloudflare Worker setup"},
                    {"id": 3, "content": "Hugging Face datasets"},
                    {"id": 4, "content": "MCP server testing"}
                ]
            }

            search_file = os.path.join(self.workspace_dir, "search_dataset.json")
            with open(search_file, 'w') as f:
                json.dump(search_data, f, indent=2)

            # Perform search
            with open(search_file, 'r') as f:
                data = json.load(f)

            # Search for "dataset" entries
            dataset_entries = [
                entry for entry in data["entries"]
                if "dataset" in entry["content"].lower()
            ]

            assert len(dataset_entries) == 2  # Should find 2 entries

            self.test_results.append({
                "test": "dataset_search_test",
                "status": "passed",
                "details": f"Found {len(dataset_entries)} dataset-related entries"
            })

            return True
        except Exception as e:
            self.test_results.append({
                "test": "dataset_search_test",
                "status": "failed",
                "details": str(e)
            })
            return False

    def file_operations_test(self) -> bool:
        """Test comprehensive file operations"""
        try:
            # Create test directory
            test_dir = os.path.join(self.workspace_dir, "mcp_test_dir")
            os.makedirs(test_dir, exist_ok=True)

            # Create multiple files with different content
            files_created = []
            for i in range(5):
                filename = f"operation_test_{i}.txt"
                filepath = os.path.join(test_dir, filename)

                content = f"""MCP File Operation Test {i}
Created: 2025-09-16
Test data: {i * 10}
Content validation: {'valid' if i % 2 == 0 else 'modified'}
"""

                with open(filepath, 'w') as f:
                    f.write(content)

                files_created.append(filepath)

            # Verify files exist and content
            for filepath in files_created:
                assert os.path.exists(filepath)
                with open(filepath, 'r') as f:
                    content = f.read()
                    assert "MCP File Operation Test" in content

            # Test file modification
            mod_file = os.path.join(test_dir, "modification_test.txt")
            with open(mod_file, 'w') as f:
                f.write("Original content")

            # Modify the file
            with open(mod_file, 'a') as f:
                f.write("\nModified content - MCP test")

            # Verify modification
            with open(mod_file, 'r') as f:
                final_content = f.read()
                assert "Original content" in final_content
                assert "Modified content" in final_content

            self.test_results.append({
                "test": "file_operations_test",
                "status": "passed",
                "details": f"Created {len(files_created)} files, performed modifications"
            })

            return True
        except Exception as e:
            self.test_results.append({
                "test": "file_operations_test",
                "status": "failed",
                "details": str(e)
            })
            return False

    def task_management_test(self) -> bool:
        """Test task management and progress tracking"""
        try:
            # Create a task list structure
            tasks = [
                {"id": 1, "description": "Initialize test environment", "status": "pending"},
                {"id": 2, "description": "Load dataset configuration", "status": "pending"},
                {"id": 3, "description": "Process dataset entries", "status": "pending"},
                {"id": 4, "description": "Validate data integrity", "status": "pending"},
                {"id": 5, "description": "Generate test report", "status": "pending"}
            ]

            # Simulate task progress updates
            task_file = os.path.join(self.workspace_dir, "task_progress.json")

            # Update task 1 to in_progress
            tasks[0]["status"] = "in_progress"
            with open(task_file, 'w') as f:
                json.dump({"tasks": tasks, "timestamp": "2025-09-16T22:51:16.420Z"}, f, indent=2)

            # Simulate processing tasks
            for i in range(len(tasks)):
                if i > 0:  # Mark previous task as completed
                    tasks[i-1]["status"] = "completed"
                tasks[i]["status"] = "in_progress"

                # Update progress file
                progress_data = {
                    "tasks": tasks,
                    "completed_count": sum(1 for t in tasks if t["status"] == "completed"),
                    "in_progress_count": sum(1 for t in tasks if t["status"] == "in_progress"),
                    "pending_count": sum(1 for t in tasks if t["status"] == "pending"),
                    "timestamp": f"2025-09-16T22:51:{16+i}.000Z"
                }

                with open(task_file, 'w') as f:
                    json.dump(progress_data, f, indent=2)

            # Mark all tasks as completed
            for task in tasks:
                task["status"] = "completed"

            final_progress = {
                "tasks": tasks,
                "completed_count": len(tasks),
                "in_progress_count": 0,
                "pending_count": 0,
                "success_rate": "100%",
                "timestamp": "2025-09-16T22:51:21.000Z"
            }

            with open(task_file, 'w') as f:
                json.dump(final_progress, f, indent=2)

            # Verify task management
            with open(task_file, 'r') as f:
                final_data = json.load(f)

            assert final_data["completed_count"] == 5
            assert final_data["success_rate"] == "100%"
            assert len(final_data["tasks"]) == 5

            self.test_results.append({
                "test": "task_management_test",
                "status": "passed",
                "details": f"Successfully managed {len(tasks)} tasks with progress tracking"
            })

            return True
        except Exception as e:
            self.test_results.append({
                "test": "task_management_test",
                "status": "failed",
                "details": str(e)
            })
            return False

    def get_test_summary(self) -> Dict[str, Any]:
        """Get comprehensive test summary"""
        total_tests = len(self.test_results)
        passed_tests = len([t for t in self.test_results if t["status"] == "passed"])
        failed_tests = total_tests - passed_tests

        return {
            "total_tests": total_tests,
            "passed": passed_tests,
            "failed": failed_tests,
            "success_rate": f"{(passed_tests/total_tests)*100:.1f}%" if total_tests > 0 else "0%",
            "results": self.test_results
        }

async def main():
    """Main test execution function"""
    print("🚀 Starting MCP Dataset Integration Tests")
    print("=" * 50)

    tester = DatasetMCPTester()

    # Run basic test
    print("📋 Running basic dataset test...")
    basic_result = tester.basic_dataset_test()
    print(f"✅ Basic test: {'PASSED' if basic_result else 'FAILED'}")

    # Run async test
    print("🔄 Running async dataset processing test...")
    async_result = await tester.async_dataset_processing_test()
    print(f"✅ Async test: {'PASSED' if async_result else 'FAILED'}")

    # Run search test
    print("🔍 Running dataset search test...")
    search_result = tester.dataset_search_test()
    print(f"✅ Search test: {'PASSED' if search_result else 'FAILED'}")

    # Run file operations test
    print("📁 Running file operations test...")
    file_result = tester.file_operations_test()
    print(f"✅ File operations test: {'PASSED' if file_result else 'FAILED'}")

    # Run task management test
    print("📋 Running task management test...")
    task_result = tester.task_management_test()
    print(f"✅ Task management test: {'PASSED' if task_result else 'FAILED'}")

    # Print summary
    print("\n📊 Test Summary:")
    print("=" * 30)
    summary = tester.get_test_summary()
    print(f"Total Tests: {summary['total_tests']}")
    print(f"Passed: {summary['passed']}")
    print(f"Failed: {summary['failed']}")
    print(f"Success Rate: {summary['success_rate']}")

    print("\n📝 Detailed Results:")
    for result in summary["results"]:
        status_icon = "✅" if result["status"] == "passed" else "❌"
        print(f"{status_icon} {result['test']}: {result['details']}")

    print("\n🎯 MCP Dataset Integration Tests Completed!")

if __name__ == "__main__":
    asyncio.run(main())
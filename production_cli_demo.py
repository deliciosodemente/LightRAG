#!/usr/bin/env python3
"""
Production-Ready CLI Demonstration Script for LightRAG Cloudflare Worker Dataset Integration

This script provides a comprehensive demonstration of Cloudflare CLI commands and workflows
for the LightRAG Cloudflare Worker Dataset Integration, with proper error handling,
user-friendly output, and production-ready features.

Features:
- Timestamp and environment information display
- Authentication workflow demonstration
- AI model and gateway command showcase
- Deployment configuration examples
- Setup script content analysis
- Error handling and recovery
- Next steps guidance
- Modular design with clear separation of concerns

Usage:
    python production_cli_demo.py
"""

import os
import sys
import subprocess
import json
from datetime import datetime
from typing import Optional, Tuple, List

# Configuration
SCRIPT_VERSION = "1.0.0"
MAX_SCRIPT_LINES = 25
SEPARATOR_LENGTH = 80

class CLIDemonstrator:
    """Production-ready CLI demonstration class"""

    def __init__(self):
        self.start_time = datetime.now()
        self.working_dir = os.getcwd()
        self.python_version = sys.version.split()[0]

    def print_header(self, title: str, emoji: str = ""):
        """Print a formatted header section"""
        separator = "=" * SEPARATOR_LENGTH
        print(f"\n{separator}")
        print(f"{title}")
        print(separator)

    def print_info(self, message: str):
        """Print informational message"""
        print(f"[INFO] {message}")

    def print_success(self, message: str):
        """Print success message"""
        print(f"[SUCCESS] {message}")

    def print_error(self, message: str):
        """Print error message"""
        print(f"[ERROR] {message}")

    def print_command(self, command: str, description: str = ""):
        """Print command with optional description"""
        if description:
            print(f"[CMD] {description}")
        print(f"Command: {command}")
        print("-" * 50)

    def run_command(self, cmd: str, description: str, check: bool = True) -> Tuple[bool, str, str]:
        """
        Run a shell command and return results

        Args:
            cmd: Command to execute
            description: Human-readable description
            check: Whether to check return code

        Returns:
            Tuple of (success, stdout, stderr)
        """
        self.print_command(cmd, description)

        try:
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                cwd=self.working_dir,
                timeout=30  # 30 second timeout
            )

            # Print output if available
            if result.stdout.strip():
                print("Output:")
                # Limit output to prevent flooding
                output_lines = result.stdout.strip().split('\n')
                for line in output_lines[:20]:  # Show first 20 lines
                    print(f"  {line}")
                if len(output_lines) > 20:
                    print(f"  ... ({len(output_lines) - 20} more lines)")

            # Print errors if any
            if result.stderr.strip() and result.returncode != 0:
                print("Errors:")
                error_lines = result.stderr.strip().split('\n')
                for line in error_lines[:10]:  # Show first 10 error lines
                    print(f"  {line}")
                if len(error_lines) > 10:
                    print(f"  ... ({len(error_lines) - 10} more error lines)")

            success = result.returncode == 0 if check else True

            if success:
                self.print_success("Command completed successfully")
            else:
                self.print_error(f"Command failed with exit code {result.returncode}")

            return success, result.stdout, result.stderr

        except subprocess.TimeoutExpired:
            self.print_error("Command timed out after 30 seconds")
            return False, "", "Timeout"
        except Exception as e:
            self.print_error(f"Error running command: {e}")
            return False, "", str(e)

    def check_file_exists(self, filepath: str) -> bool:
        """Check if file exists and provide feedback"""
        if os.path.exists(filepath):
            self.print_success(f"File found: {filepath}")
            return True
        else:
            self.print_error(f"File not found: {filepath}")
            return False

    def read_file_content(self, filepath: str, max_lines: int = MAX_SCRIPT_LINES) -> Optional[List[str]]:
        """Read and return file content with line limiting"""
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()

            # Return limited content
            content = []
            for i, line in enumerate(lines[:max_lines], 1):
                content.append("2d")

            if len(lines) > max_lines:
                content.append("... (truncated)")

            return content

        except Exception as e:
            self.print_error(f"Could not read file {filepath}: {e}")
            return None

    def demonstrate_authentication(self):
        """Demonstrate Cloudflare authentication commands"""
        self.print_header("CLOUDFLARE AUTHENTICATION")

        # Check current authentication status
        success, stdout, stderr = self.run_command(
            "npx wrangler whoami",
            "Check current authentication status"
        )

        if success and "You are logged in" in stdout:
            self.print_success("Authentication confirmed - ready to proceed")
        else:
            self.print_info("Note: Run 'npx wrangler login' if not authenticated")

        # Show login command (don't actually run it)
        print("\n[CMD] Login Command (run manually if needed):")
        print("Command: npx wrangler login")
        print("Note: This will open a browser for OAuth authentication")

    def demonstrate_ai_commands(self):
        """Demonstrate AI-related commands"""
        self.print_header("CLOUDFLARE AI COMMANDS")

        # Show available AI commands
        success, stdout, stderr = self.run_command(
            "npx wrangler ai --help",
            "Show available AI commands"
        )

        if success:
            self.print_success("AI commands available in Wrangler CLI")

        # Note about AI models command
        print("\n[CMD] AI Models Command:")
        print("Command: npx wrangler ai models")
        print("Note: Requires proper account configuration to list available models")

    def demonstrate_setup_script(self):
        """Demonstrate the setup script usage and content"""
        self.print_header("SETUP SCRIPT DEMONSTRATION")

        setup_script = "setup-cloudflare.sh"

        if self.check_file_exists(setup_script):
            print("\n[CMD] Available setup commands:")
            print("./setup-cloudflare.sh                 # Setup with defaults")
            print("./setup-cloudflare.sh .env.local     # Setup with custom env file")
            print("./setup-cloudflare.sh .env.local my-gateway  # Custom gateway name")

            # Show the setup script content
            print("\n[FILE] Setup script contents:")
            content = self.read_file_content(setup_script, 20)
            if content:
                for line in content:
                    print(line)

    def demonstrate_deployment_commands(self):
        """Demonstrate deployment-related commands"""
        self.print_header("DEPLOYMENT COMMANDS")

        deploy_script = "deploy.sh"

        if self.check_file_exists(deploy_script):
            print("\n[CMD] Deployment commands for LightRAG:")
            print("./deploy.sh deploy .env.local         # Deploy with local config")
            print("./deploy.sh deploy .env.production    # Deploy with production config")
            print("docker-compose up -d                  # Start services")
            print("docker-compose logs -f lightrag       # Monitor logs")

            # Show deployment script content
            print("\n[FILE] Deploy script contents:")
            content = self.read_file_content(deploy_script, 15)
            if content:
                for line in content:
                    print(line)

    def demonstrate_monitoring_commands(self):
        """Demonstrate monitoring and logging commands"""
        self.print_header("MONITORING COMMANDS")

        print("[CMD] Monitoring commands:")
        print("npx wrangler tail                    # Tail worker logs")
        print("docker-compose logs -f lightrag      # Monitor LightRAG logs")
        print("docker-compose ps                    # Show running services")
        print("docker stats                         # Show resource usage")

        # Test docker-compose availability
        success, stdout, stderr = self.run_command(
            "docker-compose --version",
            "Check Docker Compose availability",
            check=False
        )

    def show_integration_workflow(self):
        """Show the complete integration workflow"""
        self.print_header("COMPLETE INTEGRATION WORKFLOW")

        workflow = [
            ("1. Authentication", "npx wrangler login"),
            ("2. Verify Account", "npx wrangler whoami"),
            ("3. Setup AI Gateway", "./setup-cloudflare.sh"),
            ("4. Configure Environment", "cp .env.example .env && edit .env"),
            ("5. Test Integration", "python test_connectivity.py"),
            ("6. Run Demo", "python examples/lightrag_hf_cloudflare_dataset_demo.py"),
            ("7. Deploy Production", "./deploy.sh deploy .env.production"),
            ("8. Monitor Logs", "docker-compose logs -f lightrag"),
        ]

        for step, command in workflow:
            print("30")

    def create_integration_summary(self):
        """Create a summary of the integration"""
        self.print_header("INTEGRATION SUMMARY")

        summary = {
            "Project": "LightRAG Cloudflare Worker Dataset Integration",
            "Version": SCRIPT_VERSION,
            "Components": [
                "LightRAG core framework",
                "Cloudflare Workers AI",
                "Hugging Face datasets",
                "Docker deployment",
                "Comprehensive testing suite"
            ],
            "Key Features": [
                "Seamless AI model integration",
                "Dataset loading and processing",
                "Robust error handling",
                "Production deployment ready",
                "Monitoring and logging"
            ],
            "CLI Tools Used": [
                "npx wrangler (Cloudflare CLI)",
                "docker-compose (Container orchestration)",
                "python (Script execution)",
                "git (Version control)"
            ]
        }

        for key, value in summary.items():
            print(f"\n{key}:")
            if isinstance(value, list):
                for item in value:
                    print(f"  • {item}")
            else:
                print(f"  {value}")

    def show_next_steps(self):
        """Show next steps guidance"""
        self.print_header("NEXT STEPS")

        steps = [
            "1. Run: npx wrangler login (if not authenticated)",
            "2. Run: ./setup-cloudflare.sh (to setup AI gateway)",
            "3. Run: python test_connectivity.py (to test integration)",
            "4. Run: python examples/lightrag_hf_cloudflare_dataset_demo.py (to run demo)",
            "5. Monitor: docker-compose logs -f lightrag (for production monitoring)"
        ]

        for step in steps:
            print(step)

        print("\nFor detailed documentation, see:")
        print("- README_CLOUDFLARE_DATASET.md")
        print("- LIGHTRAG_CLOUDFLARE_DATASET_INTEGRATION_GUIDE.md")

    def run_demonstration(self):
        """Run the complete CLI demonstration"""
        print("LightRAG Cloudflare Worker Dataset Integration - Production CLI Demo")
        print("=" * SEPARATOR_LENGTH)
        print(f"Timestamp: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Working Directory: {self.working_dir}")
        print(f"Python Version: {self.python_version}")
        print(f"Script Version: {SCRIPT_VERSION}")
        print("=" * SEPARATOR_LENGTH)

        # Run all demonstrations
        try:
            self.demonstrate_authentication()
            self.demonstrate_ai_commands()
            self.demonstrate_setup_script()
            self.demonstrate_deployment_commands()
            self.demonstrate_monitoring_commands()
            self.show_integration_workflow()
            self.create_integration_summary()
            self.show_next_steps()

            # Calculate duration
            end_time = datetime.now()
            duration = end_time - self.start_time

            print("\n" + "=" * SEPARATOR_LENGTH)
            self.print_success("CLI Demonstration Complete!")
            print(f"Duration: {duration.total_seconds():.2f} seconds")
            print("=" * SEPARATOR_LENGTH)

        except KeyboardInterrupt:
            print("\n[INFO] Demonstration interrupted by user")
        except Exception as e:
            self.print_error(f"Demonstration failed: {e}")
            return False

        return True

def main():
    """Main entry point"""
    try:
        demonstrator = CLIDemonstrator()
        success = demonstrator.run_demonstration()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"[FATAL ERROR] {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
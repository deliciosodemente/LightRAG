#!/usr/bin/env python3
"""
Cloudflare CLI Demonstration for LightRAG Cloudflare Worker Dataset Integration

This script demonstrates the key Cloudflare CLI commands used in the integration,
showing how to authenticate, manage AI resources, and monitor usage for the
LightRAG Cloudflare Worker Dataset Integration.

Usage:
    python cloudflare_cli_demo.py
"""

import os
import sys
import subprocess
import json
from datetime import datetime

def run_command(cmd, description, check=True):
    """Run a shell command and return the result"""
    print(f"\n[CMD] {description}")
    print(f"Command: {cmd}")
    print("-" * 50)

    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=os.getcwd())

        if result.stdout:
            print("Output:")
            print(result.stdout)

        if result.stderr and result.returncode != 0:
            print("Errors:")
            print(result.stderr)

        if check and result.returncode != 0:
            print(f"[ERROR] Command failed with exit code {result.returncode}")
            return False

        print("[SUCCESS] Command completed successfully")
        return True

    except Exception as e:
        print(f"[ERROR] Error running command: {e}")
        return False

def demonstrate_authentication():
    """Demonstrate Cloudflare authentication commands"""
    print("\n" + "="*60)
    print("CLOUDFLARE AUTHENTICATION")
    print("="*60)

    # Check current authentication status
    run_command("npx wrangler whoami", "Check current authentication status")

    # Show login command (don't actually run it)
    print("\n[CMD] Login Command (run manually if needed):")
    print("Command: npx wrangler login")
    print("Note: This will open a browser for OAuth authentication")

def demonstrate_ai_commands():
    """Demonstrate AI-related commands"""
    print("\n" + "="*60)
    print("CLOUDFLARE AI COMMANDS")
    print("="*60)

    # Show available AI commands
    run_command("npx wrangler ai --help", "Show available AI commands")

    # Note about AI models command
    print("\n[CMD] AI Models Command:")
    print("Command: npx wrangler ai models")
    print("Note: Requires proper account configuration")
    print("This command lists available AI models in your account")

def demonstrate_setup_script():
    """Demonstrate the setup script usage"""
    print("\n" + "="*60)
    print("SETUP SCRIPT DEMONSTRATION")
    print("="*60)

    print("[CMD] Available setup commands:")
    print("./setup-cloudflare.sh                 # Setup with defaults")
    print("./setup-cloudflare.sh .env.local     # Setup with custom env file")
    print("./setup-cloudflare.sh .env.local my-gateway  # Custom gateway name")

    # Show the setup script content
    if os.path.exists("setup-cloudflare.sh"):
        print("\n[FILE] Setup script contents:")
        try:
            with open("setup-cloudflare.sh", "r") as f:
                lines = f.readlines()[:20]  # Show first 20 lines
                for i, line in enumerate(lines, 1):
                    print("2d")
                if len(lines) == 20:
                    print("... (truncated)")
        except Exception as e:
            print(f"Could not read setup script: {e}")
    else:
        print("[ERROR] setup-cloudflare.sh not found in current directory")

def demonstrate_deployment_commands():
    """Demonstrate deployment-related commands"""
    print("\n" + "="*60)
    print("DEPLOYMENT COMMANDS")
    print("="*60)

    print("[CMD] Deployment commands for LightRAG:")
    print("./deploy.sh deploy .env.local         # Deploy with local config")
    print("./deploy.sh deploy .env.production    # Deploy with production config")
    print("docker-compose up -d                  # Start services")
    print("docker-compose logs -f lightrag       # Monitor logs")

    # Show deployment script if it exists
    if os.path.exists("deploy.sh"):
        print("\n[FILE] Deploy script contents:")
        try:
            with open("deploy.sh", "r") as f:
                lines = f.readlines()[:15]  # Show first 15 lines
                for i, line in enumerate(lines, 1):
                    print("2d")
                if len(lines) == 15:
                    print("... (truncated)")
        except Exception as e:
            print(f"Could not read deploy script: {e}")
    else:
        print("[ERROR] deploy.sh not found in current directory")

def demonstrate_monitoring_commands():
    """Demonstrate monitoring and logging commands"""
    print("\n" + "="*60)
    print("MONITORING COMMANDS")
    print("="*60)

    print("[CMD] Monitoring commands:")
    print("npx wrangler tail                    # Tail worker logs")
    print("docker-compose logs -f lightrag      # Monitor LightRAG logs")
    print("docker-compose ps                    # Show running services")
    print("docker stats                         # Show resource usage")

def show_integration_workflow():
    """Show the complete integration workflow"""
    print("\n" + "="*60)
    print("COMPLETE INTEGRATION WORKFLOW")
    print("="*60)

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

def create_integration_summary():
    """Create a summary of the integration"""
    print("\n" + "="*60)
    print("INTEGRATION SUMMARY")
    print("="*60)

    summary = {
        "Project": "LightRAG Cloudflare Worker Dataset Integration",
        "Version": "1.0.0",
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

def main():
    """Main demonstration function"""
    print("LightRAG Cloudflare Worker Dataset Integration - CLI Demonstration")
    print("="*80)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Working Directory: {os.getcwd()}")
    print(f"Python Version: {sys.version}")
    print("="*80)

    # Run demonstrations
    demonstrate_authentication()
    demonstrate_ai_commands()
    demonstrate_setup_script()
    demonstrate_deployment_commands()
    demonstrate_monitoring_commands()
    show_integration_workflow()
    create_integration_summary()

    print("\n" + "="*80)
    print("CLI Demonstration Complete!")
    print("="*80)
    print("\nNext Steps:")
    print("1. Run: npx wrangler login (if not authenticated)")
    print("2. Run: ./setup-cloudflare.sh (to setup AI gateway)")
    print("3. Run: python test_connectivity.py (to test integration)")
    print("4. Run: python examples/lightrag_hf_cloudflare_dataset_demo.py (to run demo)")
    print("\nFor detailed documentation, see:")
    print("- README_CLOUDFLARE_DATASET.md")
    print("- LIGHTRAG_CLOUDFLARE_DATASET_INTEGRATION_GUIDE.md")

if __name__ == "__main__":
    main()
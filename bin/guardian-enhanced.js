#!/usr/bin/env node
/**
 * 🛡️ Guardian Enhanced CLI
 * Entry point for the enhanced Guardian system
 */

const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

// Check if Python is available
function checkPython() {
    return new Promise((resolve) => {
        const python = spawn('python3', ['--version']);
        python.on('close', (code) => {
            resolve(code === 0);
        });
        python.on('error', () => resolve(false));
    });
}

// Run JavaScript scanner (fallback)
function runJSScanner(projectPath, outputPath) {
    console.log('🛡️ Running JavaScript scanner...');
    const { GuardianScanner } = require('../src/scanner.js');
    
    const scanner = new GuardianScanner(projectPath);
    scanner.scan();
    const result = scanner.save(outputPath);
    
    console.log('\n✅ Guardian snapshot generated (JavaScript version)');
    console.log(`📁 Saved to: ${result}`);
}

// Run Python enhanced scanner
function runPythonScanner(projectPath, outputPath, args) {
    console.log('🛡️ Running Enhanced Python scanner...');
    
    const scriptPath = path.join(__dirname, '..', 'src', 'guardian_enhanced.py');
    const pythonArgs = [scriptPath, projectPath];
    
    if (outputPath) {
        pythonArgs.push('--output', outputPath);
    }
    
    // Add additional arguments
    if (args.includes('--no-quality')) {
        pythonArgs.push('--no-quality');
    }
    
    const python = spawn('python3', pythonArgs, {
        stdio: 'inherit'
    });
    
    python.on('close', (code) => {
        if (code !== 0) {
            console.error('\n❌ Python scanner failed');
            process.exit(code);
        }
    });
}

// Main
async function main() {
    const args = process.argv.slice(2);
    
    // Parse arguments
    let projectPath = '.';
    let outputPath = null;
    
    for (let i = 0; i < args.length; i++) {
        if (args[i] === '--output' || args[i] === '-o') {
            outputPath = args[i + 1];
            i++;
        } else if (args[i] === '--help' || args[i] === '-h') {
            console.log(`
🛡️ Guardian Enhanced - AI Agent Memory & Decision Support System

Usage:
  guardian-enhanced [project_path] [options]

Options:
  --output, -o <path>    Output path for guardian file
  --no-quality          Skip quality control scan (faster)
  --help, -h            Show this help message

Examples:
  guardian-enhanced                    # Scan current directory
  guardian-enhanced ./my-project       # Scan specific project
  guardian-enhanced -o custom.mdc      # Custom output path
  guardian-enhanced --no-quality       # Skip quality checks

Features:
  ✅ Project snapshot and memory
  ✅ Decision locking and conflict detection
  ✅ Technology recommendations
  ✅ Quality control (dead code, duplicates)
  ✅ Health monitoring
  ✅ Multi-IDE support (Cursor, Windsurf, Copilot, Claude)
`);
            process.exit(0);
        } else if (!args[i].startsWith('--')) {
            projectPath = args[i];
        }
    }
    
    // Check if project path exists
    if (!fs.existsSync(projectPath)) {
        console.error(`❌ Error: Project path not found: ${projectPath}`);
        process.exit(1);
    }
    
    // Check Python availability
    const hasPython = await checkPython();
    
    if (hasPython) {
        // Use enhanced Python version
        runPythonScanner(projectPath, outputPath, args);
    } else {
        // Fallback to JavaScript version
        console.log('⚠️ Python not found. Using JavaScript scanner (basic features only)');
        console.log('💡 Install Python 3 for full features (memory, quality control, etc.)');
        runJSScanner(projectPath, outputPath);
    }
}

main().catch(err => {
    console.error('❌ Error:', err.message);
    process.exit(1);
});

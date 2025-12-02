"""
GUI for Requirements Input
Author: [Your Name] - [Student ID]

Simple Tkinter GUI for inputting requirements and displaying results.
"""

import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
import threading
import json


def launch_gui(orchestrator):
    """
    Launch the GUI for the multi-agent system.

    Args:
        orchestrator: The Orchestrator instance to use
    """


    class MCPGeneratorGUI:
        """GUI application for the MCP code generator."""

        def __init__(self, master, orchestrator):
            self.master = master
            self.orchestrator = orchestrator
            self.master.title("Music Scale Trainer - AI Code Generator")
            self.master.geometry("1000x700")

            self.create_widgets()
            self.load_default_requirements()

        def create_widgets(self):
            """Create all GUI widgets."""

            # Title
            title_label = tk.Label(
                self.master,
                text = "Music Scale Trainer - AI Code Generation System",
                font = ("Arial", 16, "bold"),
                pady = 10
            )
            title_label.pack()

            # Subtitle
            subtitle_label = tk.Label(
                self.master,
                text = "Multi-Agent System with Model Context Protocol (MCP)",
                font = ("Arial", 10),
                fg = "gray"
            )
            subtitle_label.pack()

            # Requirements input section
            req_frame = tk.LabelFrame(
                self.master,
                text = "Input Requirements",
                padx = 10,
                pady = 10
            )
            req_frame.pack(fill = "both", expand = True, padx = 10, pady = 5)

            self.requirements_text = scrolledtext.ScrolledText(
                req_frame,
                height = 10,
                wrap = tk.WORD,
                font = ("Courier", 10)
            )
            self.requirements_text.pack(fill = "both", expand = True)

            # Generate button
            button_frame = tk.Frame(self.master)
            button_frame.pack(pady = 10)

            self.generate_btn = tk.Button(
                button_frame,
                text = "🚀 Generate Code & Tests",
                command = self.generate_code,
                font = ("Arial", 12, "bold"),
                bg = "#4CAF50",
                fg = "white",
                padx = 20,
                pady = 10
            )
            self.generate_btn.pack(side = tk.LEFT, padx = 5)

            self.clear_btn = tk.Button(
                button_frame,
                text = "Clear Output",
                command = self.clear_output,
                font = ("Arial", 10),
                padx = 10,
                pady = 5
            )
            self.clear_btn.pack(side = tk.LEFT, padx = 5)

            # Progress bar
            self.progress = ttk.Progressbar(
                self.master,
                mode = 'indeterminate',
                length = 300
            )
            self.progress.pack(pady = 5)

            # Status label
            self.status_label = tk.Label(
                self.master,
                text = "Ready to generate code",
                font = ("Arial", 9),
                fg = "gray"
            )
            self.status_label.pack()

            # Output section
            output_frame = tk.LabelFrame(
                self.master,
                text = "Generation Results & Status",
                padx = 10,
                pady = 10
            )
            output_frame.pack(fill = "both", expand = True, padx = 10, pady = 5)

            self.output_text = scrolledtext.ScrolledText(
                output_frame,
                height = 15,
                wrap = tk.WORD,
                font = ("Courier", 9),
                bg = "#f5f5f5"
            )
            self.output_text.pack(fill = "both", expand = True)

        def load_default_requirements(self):
            """Load default MST requirements."""
            default_req = """MST (Music Scale Trainer) is a software application designed to help musicians and music enthusiasts practice and improve their knowledge of musical scales. It provides interactive exercises where users can identify and play different scales on their instrument of choice. The software offers a variety of difficulty levels, real-time feedback on accuracy, and educational resources with explanations and audio examples of each scale. Users can track their progress and aim to master all major and minor scales."""

            self.requirements_text.insert("1.0", default_req)

        def generate_code(self):
            """Generate code in a separate thread to keep GUI responsive."""
            # Get requirements
            requirements = self.requirements_text.get("1.0", tk.END).strip()

            if not requirements:
                messagebox.showerror("Error", "Please enter requirements!")
                return

            # Disable button during generation
            self.generate_btn.config(state = tk.DISABLED)
            self.progress.start()
            self.status_label.config(text = "Generating code... This may take 1-2 minutes")

            # Run in thread
            thread = threading.Thread(
                target = self._generate_in_thread,
                args = (requirements,)
            )
            thread.start()

        def _generate_in_thread(self, requirements):
            """Run generation in background thread."""
            try:
                # Clear output
                self.output_text.delete("1.0", tk.END)
                self.log_output("Starting multi-agent workflow...\n")

                # Run workflow
                result = self.orchestrator.run_workflow(requirements)

                # Display results
                self.log_output("\n" + "=" * 60 + "\n")
                self.log_output("✅ GENERATION COMPLETE!\n")
                self.log_output("=" * 60 + "\n\n")

                self.log_output("📁 Generated Files:\n")
                self.log_output("  • generated/mst_app.py - Main application code\n")
                self.log_output("  • generated/test_mst_generated.py - Test cases\n")
                self.log_output("  • reports/model_usage.json - Usage statistics\n\n")

                self.log_output("📊 Model Usage Statistics:\n")
                usage_json = json.dumps(result["usage_stats"], indent = 2)
                self.log_output(usage_json + "\n\n")

                self.log_output("🔧 To run the generated code:\n")
                self.log_output("  python generated/mst_app.py\n\n")

                self.log_output("🧪 To run the tests:\n")
                self.log_output("  python run_tests.py\n\n")

                self.log_output("📨 MCP Messages Exchanged: {}\n".format(
                    len(result["mcp_message_history"])
                ))

                self.master.after(0, self._generation_complete)

            except Exception as e:
                self.log_output(f"\n❌ ERROR: {str(e)}\n")
                self.master.after(0, self._generation_complete)

        def log_output(self, text):
            """Thread-safe output logging."""
            self.master.after(0, lambda: self.output_text.insert(tk.END, text))
            self.master.after(0, lambda: self.output_text.see(tk.END))

        def _generation_complete(self):
            """Re-enable UI after generation."""
            self.generate_btn.config(state = tk.NORMAL)
            self.progress.stop()
            self.status_label.config(text = "Generation complete! Check 'generated' folder.")

        def clear_output(self):
            """Clear the output text area."""
            self.output_text.delete("1.0", tk.END)
            self.status_label.config(text = "Output cleared. Ready to generate.")


    # Create and run GUI
    root = tk.Tk()
    app = MCPGeneratorGUI(root, orchestrator)
    root.mainloop()
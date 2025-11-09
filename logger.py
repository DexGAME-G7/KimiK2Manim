"""
Enhanced logging utility for KimiK2Manim pipeline.

Provides:
- Timestamped logs
- Progress indicators/spinners during API calls
- Structured logging levels
- Pipeline progress tracking
- Elapsed time tracking
- Color-coded output (optional)
"""

import sys
import time
import platform
from contextlib import contextmanager
from datetime import datetime
from typing import Optional
from threading import Thread


class PipelineLogger:
    """Enhanced logger for pipeline processing and API calls."""
    
    # ANSI color codes (works on most terminals)
    COLORS = {
        'RESET': '\033[0m',
        'BOLD': '\033[1m',
        'DIM': '\033[2m',
        'BLUE': '\033[94m',
        'GREEN': '\033[92m',
        'YELLOW': '\033[93m',
        'RED': '\033[91m',
        'CYAN': '\033[96m',
        'MAGENTA': '\033[95m',
    }
    
    # Unicode-safe characters (fallback to ASCII on Windows)
    _is_windows = platform.system() == 'Windows'
    _use_unicode = not _is_windows or sys.stdout.encoding and 'utf' in sys.stdout.encoding.lower()
    
    def __init__(self, use_colors: bool = True, verbose: bool = True):
        """
        Initialize logger.
        
        Args:
            use_colors: Whether to use ANSI color codes
            verbose: Whether to show verbose logs
        """
        self.use_colors = use_colors and sys.stdout.isatty()
        self.verbose = verbose
        self.start_time = time.time()
        self.api_call_count = 0
        self.total_api_time = 0.0
        
        # Use ASCII-safe characters on Windows
        if self._use_unicode:
            self.checkmark = "✓"
            self.cross = "✗"
            self.spinner_chars = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
            self.progress_filled = '█'
            self.progress_empty = '░'
        else:
            self.checkmark = "[OK]"
            self.cross = "[FAIL]"
            self.spinner_chars = ['|', '/', '-', '\\']
            self.progress_filled = '#'
            self.progress_empty = '-'
        
    def _colorize(self, text: str, color: str) -> str:
        """Apply color to text if colors are enabled."""
        if not self.use_colors:
            return text
        return f"{self.COLORS.get(color, '')}{text}{self.COLORS['RESET']}"
    
    def _timestamp(self) -> str:
        """Get formatted timestamp."""
        return datetime.now().strftime("%H:%M:%S")
    
    def _elapsed(self) -> str:
        """Get elapsed time since logger start."""
        elapsed = time.time() - self.start_time
        if elapsed < 60:
            return f"{elapsed:.1f}s"
        elif elapsed < 3600:
            return f"{elapsed/60:.1f}m"
        else:
            return f"{elapsed/3600:.1f}h"
    
    def info(self, message: str, prefix: str = "INFO"):
        """Log info message."""
        timestamp = self._timestamp()
        elapsed = self._elapsed()
        colored_prefix = self._colorize(f"[{prefix}]", "BLUE")
        print(f"{timestamp} {colored_prefix} {message} {self._colorize(f'({elapsed})', 'DIM')}")
        sys.stdout.flush()
    
    def success(self, message: str, prefix: str = None):
        """Log success message."""
        timestamp = self._timestamp()
        elapsed = self._elapsed()
        if prefix is None:
            prefix = self.checkmark
        colored_prefix = self._colorize(f"[{prefix}]", "GREEN")
        print(f"{timestamp} {colored_prefix} {message} {self._colorize(f'({elapsed})', 'DIM')}")
        sys.stdout.flush()
    
    def warning(self, message: str, prefix: str = "WARN"):
        """Log warning message."""
        timestamp = self._timestamp()
        elapsed = self._elapsed()
        colored_prefix = self._colorize(f"[{prefix}]", "YELLOW")
        print(f"{timestamp} {colored_prefix} {message} {self._colorize(f'({elapsed})', 'DIM')}")
        sys.stdout.flush()
    
    def error(self, message: str, prefix: str = "ERROR"):
        """Log error message."""
        timestamp = self._timestamp()
        elapsed = self._elapsed()
        colored_prefix = self._colorize(f"[{prefix}]", "RED")
        print(f"{timestamp} {colored_prefix} {message} {self._colorize(f'({elapsed})', 'DIM')}")
        sys.stdout.flush()
    
    def debug(self, message: str, prefix: str = "DEBUG"):
        """Log debug message (only if verbose)."""
        if not self.verbose:
            return
        timestamp = self._timestamp()
        elapsed = self._elapsed()
        colored_prefix = self._colorize(f"[{prefix}]", "DIM")
        print(f"{timestamp} {colored_prefix} {message} {self._colorize(f'({elapsed})', 'DIM')}")
        sys.stdout.flush()
    
    def stage(self, stage_name: str, stage_num: int, total_stages: int):
        """Log pipeline stage start."""
        timestamp = self._timestamp()
        elapsed = self._elapsed()
        stage_info = self._colorize(f"[{stage_num}/{total_stages}]", "CYAN")
        print(f"\n{timestamp} {stage_info} {self._colorize(stage_name, 'BOLD')} {self._colorize(f'({elapsed})', 'DIM')}")
        sys.stdout.flush()
    
    def api_call_start(self, model: str, details: Optional[dict] = None):
        """Log API call start."""
        self.api_call_count += 1
        timestamp = self._timestamp()
        elapsed = self._elapsed()
        call_num = self._colorize(f"#{self.api_call_count}", "MAGENTA")
        model_name = self._colorize(model, "CYAN")
        
        print(f"\n{timestamp} {call_num} {self._colorize('[API CALL]', 'BLUE')} Requesting {model_name} {self._colorize(f'({elapsed})', 'DIM')}")
        
        if details and self.verbose:
            for key, value in details.items():
                if value:
                    print(f"  {self._colorize(key + ':', 'DIM')} {value}")
        sys.stdout.flush()
    
    def api_call_end(self, success: bool = True, usage: Optional[dict] = None, duration: Optional[float] = None):
        """Log API call completion."""
        timestamp = self._timestamp()
        elapsed = self._elapsed()
        
        if success:
            status = self._colorize(f"{self.checkmark} Success", "GREEN")
        else:
            status = self._colorize(f"{self.cross} Failed", "RED")
        
        info_parts = [status]
        
        if duration is not None:
            self.total_api_time += duration
            info_parts.append(self._colorize(f"{duration:.2f}s", "DIM"))
        
        if usage:
            prompt_tokens = usage.get('prompt_tokens', 0)
            completion_tokens = usage.get('completion_tokens', 0)
            total_tokens = usage.get('total_tokens', 0)
            if total_tokens > 0:
                info_parts.append(f"{total_tokens} tokens ({prompt_tokens}+{completion_tokens})")
        
        print(f"{timestamp} {self._colorize('[API RESPONSE]', 'BLUE')} {' | '.join(info_parts)} {self._colorize(f'({elapsed})', 'DIM')}")
        sys.stdout.flush()
    
    def progress(self, current: int, total: int, item_name: str = "items"):
        """Log progress for batch operations."""
        percentage = (current / total * 100) if total > 0 else 0
        bar_length = 30
        filled = int(bar_length * current / total) if total > 0 else 0
        bar = self.progress_filled * filled + self.progress_empty * (bar_length - filled)
        
        timestamp = self._timestamp()
        progress_info = self._colorize(f"[{current}/{total}]", "CYAN")
        bar_display = self._colorize(bar, "GREEN")
        percentage_display = self._colorize(f"{percentage:.1f}%", "YELLOW")
        
        print(f"\r{timestamp} {progress_info} {bar_display} {percentage_display} {item_name}", end='', flush=True)
        
        if current >= total:
            print()  # New line when complete
    
    @contextmanager
    def api_call(self, model: str, details: Optional[dict] = None, show_spinner: bool = True):
        """
        Context manager for API calls with automatic progress indication.
        
        Usage:
            with logger.api_call("kimi-k2", {"messages": 3}) as call_info:
                response = client.chat.completions.create(...)
                call_info['usage'] = response.usage  # Optional: add usage info
        """
        self.api_call_start(model, details)
        start_time = time.time()
        call_info = {'success': True, 'usage': None, 'duration': None}
        
        spinner_stop = [False]  # Use list for mutable reference
        spinner_thread = None
        if show_spinner:
            spinner_thread = Thread(target=self._spinner, args=(lambda: spinner_stop[0],), daemon=True)
            spinner_thread.start()
        
        try:
            yield call_info
            call_info['success'] = True
        except Exception as e:
            call_info['success'] = False
            self.error(f"API call failed: {str(e)}")
            raise
        finally:
            spinner_stop[0] = True
            if spinner_thread:
                spinner_thread.join(timeout=0.2)
            duration = time.time() - start_time
            call_info['duration'] = duration
            self.api_call_end(
                success=call_info['success'], 
                usage=call_info.get('usage'),
                duration=duration
            )
    
    def _spinner(self, stop_flag):
        """Show spinner animation during API calls."""
        i = 0
        while not stop_flag():
            char = self.spinner_chars[i % len(self.spinner_chars)]
            spinner_text = f"\r  {self._colorize(char, 'CYAN')} Waiting for API response..."
            try:
                print(spinner_text, end='', flush=True)
            except UnicodeEncodeError:
                # Fallback to ASCII if Unicode fails
                print(f"\r  [{char}] Waiting for API response...", end='', flush=True)
            time.sleep(0.1)
            i += 1
        # Clear spinner line
        print("\r" + " " * 50 + "\r", end='', flush=True)
    
    def summary(self):
        """Print summary statistics."""
        total_time = time.time() - self.start_time
        avg_api_time = self.total_api_time / self.api_call_count if self.api_call_count > 0 else 0
        
        print(f"\n{self._colorize('=' * 70, 'CYAN')}")
        print(f"{self._colorize('Pipeline Summary', 'BOLD')}")
        print(f"{self._colorize('=' * 70, 'CYAN')}")
        print(f"  Total time: {self._colorize(f'{total_time:.2f}s', 'GREEN')}")
        print(f"  API calls: {self._colorize(str(self.api_call_count), 'CYAN')}")
        print(f"  Total API time: {self._colorize(f'{self.total_api_time:.2f}s', 'CYAN')}")
        if self.api_call_count > 0:
            print(f"  Avg API time: {self._colorize(f'{avg_api_time:.2f}s', 'CYAN')}")
        print(f"{self._colorize('=' * 70, 'CYAN')}\n")


# Global logger instance
_default_logger: Optional[PipelineLogger] = None


def get_logger(use_colors: bool = True, verbose: bool = True) -> PipelineLogger:
    """Get or create global logger instance."""
    global _default_logger
    if _default_logger is None:
        _default_logger = PipelineLogger(use_colors=use_colors, verbose=verbose)
    return _default_logger


def reset_logger():
    """Reset the global logger (useful for testing)."""
    global _default_logger
    _default_logger = None


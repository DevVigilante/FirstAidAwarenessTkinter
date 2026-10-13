import tkinter as tk
from tkinter import ttk
from config import APP_VERSION, FONT_UI, FONT_UI_SYMBOL, BG, CARD, TEXT, MUTED, PRIMARY, PRIMARY_DARK, BORDER, DANGER
import sys

def setup_style(root):
    style = ttk.Style(root)
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass

    style.configure("TFrame", background=BG)
    style.configure("Card.TFrame", background=CARD)
    style.configure("TLabel", background=BG, foreground=TEXT, font=(FONT_UI, 10))
    style.configure("Title.TLabel", background=BG, foreground=TEXT,
                    font=(FONT_UI, 22, "bold"))
    style.configure("Subtitle.TLabel", background=BG, foreground=MUTED,
                    font=(FONT_UI, 11))
    style.configure("Section.TLabel", background=BG, foreground=TEXT,
                    font=(FONT_UI, 15, "bold"))
    style.configure("CardTitle.TLabel", background=CARD, foreground=TEXT,
                    font=(FONT_UI, 12, "bold"))
    style.configure("CardText.TLabel", background=CARD, foreground=MUTED,
                    font=(FONT_UI, 9))
    style.configure("Body.TLabel", background=BG, foreground=TEXT,
                    font=(FONT_UI, 10))
    style.configure("Muted.TLabel", background=BG, foreground=MUTED,
                    font=(FONT_UI, 9))
    style.configure("TButton", font=(FONT_UI, 10, "bold"), padding=(12, 8))
    style.configure("Primary.TButton", background=PRIMARY, foreground="white",
                    padding=(14, 9))
    style.map("Primary.TButton",
              background=[("active", PRIMARY_DARK)],
              foreground=[("active", "white")])
    style.configure("Danger.TButton", background=DANGER, foreground="white",
                    padding=(14, 9))
    style.map("Danger.TButton",
              background=[("active", "#9f1f1f")],
              foreground=[("active", "white")])
    style.configure("TEntry", padding=8)
    style.configure("TRadiobutton", background=BG, foreground=TEXT,
                    font=(FONT_UI, 10))
    style.configure("TCheckbutton", background=BG, foreground=TEXT)


def add_header(parent, title, subtitle=None, icon="✚"):
    frame = ttk.Frame(parent)
    frame.pack(fill="x", padx=28, pady=(22, 8))
    top = ttk.Frame(frame)
    top.pack(fill="x")
    ttk.Label(top, text=f"{icon}  {title}", style="Title.TLabel").pack(side="left")
    ttk.Label(top, text=f"v{APP_VERSION}", style="Muted.TLabel").pack(side="right")
    if subtitle:
        ttk.Label(frame, text=subtitle, style="Subtitle.TLabel",
                  wraplength=900, justify="left").pack(fill="x", pady=(5, 0))
    return frame


def add_action_bar(parent, back_command=None, primary_text=None, primary_command=None):
    bar = ttk.Frame(parent)
    bar.pack(fill="x", padx=28, pady=(10, 20))
    if back_command:
        ttk.Button(bar, text="← Back", command=back_command).pack(side="left")
    if primary_command and primary_text:
        ttk.Button(bar, text=primary_text, command=primary_command,
                   style="Primary.TButton").pack(side="right")
    return bar


def card(parent, title, description, icon="•", command=None):
    outer = tk.Frame(parent, bg=CARD, highlightbackground=BORDER,
                     highlightthickness=1, bd=0)
    inner = tk.Frame(outer, bg=CARD)
    inner.pack(fill="both", expand=True, padx=16, pady=15)

    tk.Label(inner, text=icon, bg=CARD, fg=PRIMARY,
             font=(FONT_UI_SYMBOL, 22, "bold")).pack(anchor="w")
    tk.Label(inner, text=title, bg=CARD, fg=TEXT,
             font=(FONT_UI, 12, "bold")).pack(anchor="w", pady=(5, 3))
    tk.Label(inner, text=description, bg=CARD, fg=MUTED,
             font=(FONT_UI, 9), wraplength=250, justify="left").pack(anchor="w")

    if command:
        btn = ttk.Button(inner, text="Open →", command=command)
        btn.pack(anchor="w", pady=(12, 0))
    return outer


class ScrollableFrame(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.canvas = tk.Canvas(
            self,
            highlightthickness=0,
            borderwidth=0,
            background=BG
        )

        self.scrollbar = ttk.Scrollbar(
            self,
            orient="vertical",
            command=self.canvas.yview
        )

        self.inner = ttk.Frame(self.canvas)

        self._window_id = self.canvas.create_window(
            (0, 0),
            window=self.inner,
            anchor="nw"
        )

        self.canvas.configure(
            yscrollcommand=self.scrollbar.set
        )

        self.canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        self.scrollbar.pack(
            side="right",
            fill="y"
        )

        # Scroll state
        self._scroll_remainder = 0.0
        self._scrolling_active = False

        # Update the scrollable area when content changes.
        self.inner.bind(
            "<Configure>",
            self._update_scroll_region
        )

        # Keep the content width equal to the canvas width.
        self.canvas.bind(
            "<Configure>",
            self._update_content_width
        )

        # Activate scrolling when the pointer enters the canvas.
        self.canvas.bind(
            "<Enter>",
            self._activate_scrolling
        )

        self.canvas.bind(
            "<Leave>",
            self._deactivate_scrolling
        )

    def _update_scroll_region(self, event=None):
        self.canvas.configure(
            scrollregion=self.canvas.bbox("all")
        )

    def _update_content_width(self, event):
        self.canvas.itemconfigure(
            self._window_id,
            width=event.width
        )

    def _activate_scrolling(self, event=None):
        if self._scrolling_active:
            return

        self._scrolling_active = True

        # Windows, macOS and supported Linux touchpad events.
        self.bind_all(
            "<MouseWheel>",
            self._on_mousewheel,
            add="+"
        )

        # Linux mouse-wheel events.
        self.bind_all(
            "<Button-4>",
            self._on_linux_scroll,
            add="+"
        )

        self.bind_all(
            "<Button-5>",
            self._on_linux_scroll,
            add="+"
        )

    def _deactivate_scrolling(self, event=None):
        if not self._scrolling_active:
            return

        self._scrolling_active = False

        # Remove the global bindings.
        self.unbind_all("<MouseWheel>")
        self.unbind_all("<Button-4>")
        self.unbind_all("<Button-5>")

        # Prevent residual movement from affecting the next gesture.
        self._scroll_remainder = 0.0

    def _on_mousewheel(self, event):
        if not self.winfo_exists():
            return

        if sys.platform == "darwin":
            # macOS trackpad deltas.
            delta = -event.delta

        elif sys.platform.startswith("win"):
            # Windows wheel events normally use multiples of 120.
            delta = -event.delta / 120.0

        else:
            # Linux touchpad events, when exposed through MouseWheel.
            delta = -event.delta

        # Accumulate fractional movement.
        self._scroll_remainder += delta

        # Scroll only when a complete unit is accumulated.
        movement = int(self._scroll_remainder)

        if movement:
            self._scroll_remainder -= movement

            self.canvas.yview_scroll(
                movement,
                "units"
            )

    def _on_linux_scroll(self, event):
        if not self.winfo_exists():
            return

        # Reset fractional movement when a discrete wheel event arrives.
        self._scroll_remainder = 0.0

        if event.num == 4:
            self.canvas.yview_scroll(-1, "units")

        elif event.num == 5:
            self.canvas.yview_scroll(1, "units")

    def destroy(self):
        self._deactivate_scrolling()
        super().destroy()
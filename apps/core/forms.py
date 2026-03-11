from django import forms


class TailwindFormMixin:
    input_classes = (
        "mt-1 w-full rounded-2xl border border-slate-300 bg-white px-4 py-3 "
        "text-sm text-slate-900 shadow-sm outline-none transition focus:border-slate-900 "
        "focus:ring-2 focus:ring-slate-900/10"
    )
    textarea_classes = input_classes + " min-h-[120px]"
    select_classes = input_classes
    checkbox_classes = "h-4 w-4 rounded border-slate-300 text-amber-600 focus:ring-amber-500"
    file_classes = (
        "mt-1 block w-full text-sm text-slate-700 file:mr-4 file:rounded-full file:border-0 "
        "file:bg-slate-900 file:px-4 file:py-2 file:text-sm file:font-semibold file:text-white"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_tailwind_classes()

    def apply_tailwind_classes(self):
        for field in self.fields.values():
            widget = field.widget
            existing = widget.attrs.get("class", "")
            if isinstance(widget, forms.CheckboxInput):
                widget.attrs["class"] = f"{existing} {self.checkbox_classes}".strip()
            elif isinstance(widget, forms.Textarea):
                widget.attrs["class"] = f"{existing} {self.textarea_classes}".strip()
            elif isinstance(widget, (forms.Select, forms.SelectMultiple)):
                widget.attrs["class"] = f"{existing} {self.select_classes}".strip()
            elif isinstance(widget, forms.ClearableFileInput):
                widget.attrs["class"] = f"{existing} {self.file_classes}".strip()
            else:
                widget.attrs["class"] = f"{existing} {self.input_classes}".strip()


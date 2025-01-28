import tkinter as tk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText

# ข้อมูลเช็คชื่อ
attendance_data = {
    "ปี 1": {
        "301": ["027", "028"],
        "302": ["029", "050"],
        "304": ["030", "031", "035", "037"],
    },
    "ปี 2": {
        "307": ["015", "104"],
        "309/1": ["106", "107"],
    },
    "ปี 3": {
        "301": ["53", "55"],
        "302": ["61", "78"],
    },
}

# ฟังก์ชันสร้าง GUI
def create_attendance_gui(data):
    def submit_data():
        summary_text = ""
        for year, rooms in data.items():
            summary_text += f"** {year} **\n"
            for room, students in rooms.items():
                summary_text += f"{room} = "
                student_data = []
                for student in students:
                    reason = reasons[year][room][student].get()
                    if statuses[year][room][student].get():
                        student_data.append(f"{student} ครบ")
                    else:
                        student_data.append(f"{student} {reason}")
                summary_text += " ".join(student_data) + "\n"
        
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, summary_text)
        messagebox.showinfo("สำเร็จ", "เช็คชื่อเสร็จสิ้น! คุณสามารถคัดลอกผลลัพธ์ได้")

    root = tk.Tk()
    root.title("ระบบเช็คชื่อ")

    frame = tk.Frame(root)
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    canvas = tk.Canvas(frame)
    scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    statuses = {}
    reasons = {}

    for year, rooms in data.items():
        year_label = tk.Label(scrollable_frame, text=f"** {year} **", font=("Arial", 12, "bold"))
        year_label.pack(anchor="w", pady=5)
        statuses[year] = {}
        reasons[year] = {}
        for room, students in rooms.items():
            room_label = tk.Label(scrollable_frame, text=f"ห้อง {room}", font=("Arial", 10))
            room_label.pack(anchor="w", padx=10)
            statuses[year][room] = {}
            reasons[year][room] = {}
            for student in students:
                student_frame = tk.Frame(scrollable_frame)
                student_frame.pack(anchor="w", padx=20, pady=2)

                status_var = tk.BooleanVar(value=True)
                reason_var = tk.StringVar(value="")

                statuses[year][room][student] = status_var
                reasons[year][room][student] = reason_var

                tk.Checkbutton(student_frame, text=f"รหัส {student}", variable=status_var).pack(side="left")
                tk.Entry(student_frame, textvariable=reason_var, width=30).pack(side="left", padx=5)

    submit_button = tk.Button(root, text="บันทึกข้อมูล", command=submit_data)
    submit_button.pack(pady=10)

    result_text = ScrolledText(root, height=10)
    result_text.pack(fill="both", expand=True, padx=10, pady=10)

    root.mainloop()

# เรียกใช้งาน GUI
create_attendance_gui(attendance_data)
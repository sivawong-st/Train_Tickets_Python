import tkinter as tk

class Station:
    def __init__(self,name,number):
        self.name = name
        self.number = number

    def __str__(self):
        return f"สถานี: {self.name} หมายเลข: {self.number}"

class Ticket:
    def __init__(self,source,destination,fare):
        self.source = source
        self.destination = destination
        self.fare = fare

class TrainTicketSystem:
    def __init__(self,root):
        self.window = root
        self.window.title("Train_Tickets")
        self.window.minsize(width=1200,height=700)
        self.window.geometry("1200x700")

        self.stations = self.create_stations()
        self.selected_source = None
        self.selected_destination = None
        self.total_fare = 0
        self.paid_amount = 0
        self.trip_statistics = []
        self.revenue = []
        self.change_list = []

        self.create_widgets()

    def create_stations(self):
        station_names = ["รังสิต","หลักหก","ดอนเมือง","หลักสี่","บางเขน","จตุจักร"]
        return [Station(name,index + 1) for index,name in enumerate(station_names)]

    def create_widgets(self):
        self.window.grid_columnconfigure(0,weight=1)
        self.window.grid_columnconfigure(1,weight=1)
        self.window.grid_rowconfigure(0,weight=1)

        #เฟรมซ้าย
        left_window = tk.Frame(self.window,bg='#FF2442')
        left_window.grid(row=0,column=0,sticky="nsew")

        station_head = tk.Label(left_window,text="สถานีรถไฟฟ้าสายสีแดง",font=("Arial", 30),bg='#FFEDDA')
        station_head.pack(pady=20)

        #สร้างปุ่มสำหรับเลือกสถานี
        for station in self.stations:
            button = tk.Button(left_window,text=station.name,command=lambda name=station.name: self.select_station(name),height=2,font=("Arial", 20))
            button.pack(fill=tk.BOTH,expand=True,padx=10,pady=5)

        #เฟรมขวา
        right_window = tk.Frame(self.window,bg='#FFEDDA')
        right_window.grid(row=0,column=1,sticky="nsew")

        #Label สำหรับการแจ้งเตือน
        self.notification_label = tk.Label(right_window,text="เลือกสถานีต้นทาง:",font=("Arial", 20),bg='red',fg='white')
        self.notification_label.pack(pady=10)

        #Label สำหรับสถานีต้นทาง
        self.fstation_label = tk.Label(right_window,text="สถานีต้นทาง:",font=("Arial", 18),bg='#FFEDDA')
        self.fstation_label.pack(pady=20)

        #Label สำหรับสถานีปลายทาง
        self.lstation_label = tk.Label(right_window,text="สถานีปลายทาง:",font=("Arial", 18),bg='#FFEDDA')
        self.lstation_label.pack(pady=20)

        #Label สำหรับค่าตั๋ว
        self.fare_label = tk.Label(right_window,text="ค่าตั๋ว: 0 บาท",font=("Arial", 18),bg='#FFEDDA')
        self.fare_label.pack(pady=20)

        #Label สำหรับแสดงยอดเงินที่ใส่
        self.payment_label = tk.Label(right_window,text="ยอดเงินที่ใส่: 0 บาท",font=("Arial", 18),bg='#FFEDDA')
        self.payment_label.pack(pady=20)

        #สร้างปุ่มสำหรับใส่เงิน
        money_buttons_frame = tk.Frame(right_window,bg='#FFEDDA')
        money_buttons_frame.pack(padx=10,pady=5)

        money_values = [1,2,5,10,20,50,100,500,1000]
        for value in money_values:
            button = tk.Button(money_buttons_frame,text=str(value),command=lambda amount=value: self.add_money(amount),height=2,width=4,font=("Arial", 14))
            button.pack(side=tk.LEFT,padx=5)

        #ปุ่มยืนยันการซื้อ
        self.confirm_button = tk.Button(right_window,text="ยืนยันการซื้อ",command=self.confirm_purchase,state=tk.DISABLED,height=2,font=("Arial", 14))
        self.confirm_button.pack(padx=10,pady=5,fill=tk.X)

        #ปุ่มรับตั๋ว
        self.ticket_button = tk.Button(right_window,text="รับตั๋ว",command=self.get_ticket,state=tk.DISABLED,height=2,font=("Arial", 14))
        self.ticket_button.pack(padx=10,pady=5,fill=tk.X)

        #ปุ่มแสดงสถิติ
        stats_button = tk.Button(right_window,text="แสดงสถิติการเดินทาง",command=self.show_statistics,height=2,font=("Arial", 14))
        stats_button.pack(padx=10,pady=5,fill=tk.X)

    def select_station(self,station_name):
        if self.selected_source is None:
            self.selected_source = station_name
            self.fstation_label.config(text=f"สถานีต้นทาง: {self.selected_source}")
            self.notification_label.config(text="เลือกสถานีปลายทาง:")
        elif self.selected_destination is None:
            if station_name != self.selected_source:
                self.selected_destination = station_name
                self.lstation_label.config(text=f"สถานีปลายทาง: {self.selected_destination}")
                self.notification_label.config(text="คำนวณค่าตั๋ว...")
                self.calculate_fare()
            else:
                self.notification_label.config(text="กรุณาเลือกสถานีปลายทางที่แตกต่างจากสถานีต้นทาง")
        else:
            if station_name == self.selected_source:
                self.reset_selection()
            elif station_name == self.selected_destination:
                self.selected_destination = None
                self.lstation_label.config(text="สถานีปลายทาง:")
                self.notification_label.config(text="เลือกสถานีปลายทาง:")
                self.fare_label.config(text="ค่าตั๋ว: 0 บาท")
            else:
                self.selected_source = station_name
                self.selected_destination = None
                self.fare_label.config(text="ค่าตั๋ว: 0 บาท")
                self.fstation_label.config(text=f"สถานีต้นทาง: {self.selected_source}")
                self.lstation_label.config(text="สถานีปลายทาง:")
                self.notification_label.config(text="เลือกสถานีปลายทาง:")

    def calculate_fare(self):
        if self.selected_source is not None and self.selected_destination is not None:
            source_number = next(station.number for station in self.stations if station.name == self.selected_source)
            destination_number = next(station.number for station in self.stations if station.name == self.selected_destination)
            distance = abs(source_number - destination_number)
            self.total_fare = distance * 13  # คิดเงินตามระยะทาง (13 บาทต่อสถานี)
            self.fare_label.config(text=f"ค่าตั๋ว: {self.total_fare} บาท")
        else:
            self.fare_label.config(text="กรุณาเลือกสถานีต้นทางและปลายทาง")

    def add_money(self,amount):
        self.paid_amount += amount
        self.payment_label.config(text=f"ยอดเงินที่ใส่: {self.paid_amount} บาท")
        self.check_payment()

    def check_payment(self):
        if self.paid_amount >= self.total_fare:
            self.notification_label.config(text="ชำระเงินเสร็จสิ้น! กดปุ่มยืนยันการซื้อ.")
            self.confirm_button.config(state=tk.NORMAL)
        else:
            self.notification_label.config(text="กรุณาใส่เงินให้เพียงพอสำหรับค่าตั๋ว.")
            self.confirm_button.config(state=tk.DISABLED)

    def calculate_change(self,change):
        coins = [1000,500,100,50,20,10,5,2,1]
        change_details = {}
        
        for coin in coins:
            if change <= 0:
                break
            count = change // coin
            if count > 0:
                change_details[coin] = count
                change -= coin * count

        return change_details

    def confirm_purchase(self):
        if self.paid_amount >= self.total_fare:
            change = self.paid_amount - self.total_fare
            change_details = self.calculate_change(change)
            change_text = ", ".join([f"{v} x {k} บาท" for k, v in change_details.items()])
            
            self.notification_label.config(text=f"ชำระเงินเรียบร้อย! เงินทอน: {change} บาท ({change_text})")
            
            #บันทึกข้อมูลการเดินทางและรายรับ
            self.trip_statistics.append((self.selected_source,self.selected_destination))
            self.revenue.append(self.total_fare)
            self.change_list.append(change)
            self.save_to_file()

            self.paid_amount = 0
            self.confirm_button.config(state=tk.DISABLED)
            self.ticket_button.config(state=tk.NORMAL)

    def save_to_file(self):
        with open("trip_statistics.txt","a",encoding="utf-8") as file:
            file.write("ข้อมูลการเดินทาง:\n")
            for trip in self.trip_statistics:
                source, destination = trip
                file.write(f"{source} -> {destination}\n")
            file.write(f"\nรายรับทั้งหมด: {sum(self.revenue)} บาท\n")
            file.write(f"เงินทอนทั้งหมด: {sum(self.change_list)} บาท\n")
            file.write("="*40 + "\n")

    def get_ticket(self):
        self.notification_label.config(text="คุณได้รับตั๋วเรียบร้อยแล้ว!")
        self.reset_selection()
        self.ticket_button.config(state=tk.DISABLED)

    def reset_selection(self):
        self.selected_source = None
        self.selected_destination = None
        self.total_fare = 0
        self.paid_amount = 0
        self.fstation_label.config(text="สถานีต้นทาง:")
        self.lstation_label.config(text="สถานีปลายทาง:")
        self.fare_label.config(text="ค่าตั๋ว: 0 บาท")
        self.notification_label.config(text="เลือกสถานีต้นทาง:")
        self.payment_label.config(text="ยอดเงินที่ใส่: 0 บาท")
        self.confirm_button.config(state=tk.DISABLED)

    def show_statistics(self):
        stats_window = tk.Toplevel(self.window)
        stats_window.title("สถิติการเดินทาง")
        stats_window.geometry("400x300")
        
        stats_text = "\n"
        try:
            with open("trip_statistics.txt","r",encoding="utf-8") as file:
                stats_text += file.read()
        except FileNotFoundError:
            stats_text += "ไม่มีข้อมูลการเดินทาง"

        #Label สำหรับแสดงผล
        stats_label = tk.Label(stats_window,text=stats_text,justify=tk.LEFT,font=("Arial", 12))
        stats_label.pack(pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    ticket_system = TrainTicketSystem(root)
    root.mainloop()
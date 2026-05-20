import time

class TuringMachine:
    def __init__(self, num1, num2):
        self.tape = ['B'] * 30 + list(num1) + ['*'] + list(num2) + ['='] + ['B'] * 60
        self.head = 30 
        self.current_state = 'q0'
        self.step_count = 0
        self.num1 = num1
        self.num2 = num2
        self.shift_count = 0
        
    def log_step(self, action_desc):
        self.step_count += 1
        print(f"\nADIM: {self.step_count}")
        print(f"Durum: {self.current_state}")
        print(f"Okunan Sembol: {self.tape[self.head] if self.head < len(self.tape) else 'B'}")
        print(f"Kafa Hareketi (Konum): {self.head}")
        print(f"Yapılan İşlem: {action_desc}")
        
        start_idx = 0
        while start_idx < len(self.tape) and self.tape[start_idx] == 'B' and start_idx < self.head - 2:
            start_idx += 1
            
        end_idx = len(self.tape)
        while end_idx > start_idx and self.tape[end_idx - 1] == 'B' and end_idx > self.head + 3:
            end_idx -= 1
            
        display_tape = list(self.tape[start_idx:end_idx])
        head_in_display = self.head - start_idx
        
        if head_in_display < len(display_tape):
            display_tape[head_in_display] = f"[{display_tape[head_in_display]}]"
            
        print(f"Bant İçeriği: B{''.join(map(str, display_tape))}B")
        print("-" * 30)
        time.sleep(0.01)  

    def run(self):
        correct_dec = int(self.num1, 2) * int(self.num2, 2)
        correct_bin = bin(correct_dec)[2:]

        while self.current_state not in ['q_accept', 'q_reject']:
            char = self.tape[self.head]
            if self.current_state == 'q0':
                if char != '=':
                    self.log_step("Birinci sayı taranıyor, sağa hareket")
                    self.head += 1
                else:
                    self.log_step("'=' bulundu, sola dönülerek çarpanın son biti kontrol edilecek")
                    self.current_state = 'q1'
                    self.head -= 1
            elif self.current_state == 'q1':
                if char in ['x', 'y']:
                    self.head -= 1
                elif char == '0':
                    self.tape[self.head] = 'x'  
                    self.log_step("Çarpan biti '0' bulundu -> x yapıldı. Sonuca 0 eklenecek")
                    self.current_state = 'q2'
                    self.head += 1
                elif char == '1':
                    self.tape[self.head] = 'y' 
                    self.log_step("Çarpan biti '1' bulundu -> y yapıldı. Birinci sayı eklenecek")
                    self.current_state = 'q3'
                    self.head -= 1
                elif char == '*':
                    self.log_step("Çarpanın tüm bitleri bitti. Bant temizleniyor...")
                    self.current_state = 'q_clean'
                    self.head += 1

           
            elif self.current_state == 'q2':
                if char != 'B':
                    self.head += 1
                else:
                    self.tape[self.head] = '0'
                    self.log_step("Çarpan 0 olduğu için sonuca '0' yazıldı, sola dönülüyor")
                    self.shift_count += 1
                    while self.tape[self.head] != '=':
                        self.head -= 1
                    self.current_state = 'q9'

            elif self.current_state == 'q3':
                if char != 'B':
                    self.head -= 1  
                else:
                    self.current_state = 'q4'
                    self.head += 1

            elif self.current_state == 'q4':
                if char in ['X', 'Y']:
                    self.head += 1
                elif char == '0':
                    self.tape[self.head] = 'X'
                    self.log_step("Birinci sayıdan '0' alındı -> X yapıldı")
                    self.current_state = 'q5'
                    self.head += 1
                elif char == '1':
                    self.tape[self.head] = 'Y'
                    self.log_step("Birinci sayıdan '1' alındı -> Y yapıldı")
                    self.current_state = 'q6'
                    self.head += 1
                elif char == '*':
                    self.log_step("Birinci sayının bitleri sonuca eklendi, işaretler sıfırlanıyor")
                    self.current_state = 'q8'
                    self.head -= 1

            elif self.current_state in ['q5', 'q6']:
                write_bit = '0' if self.current_state == 'q5' else '1'
                if char != 'B':
                    self.head += 1
                else:
                    self.tape[self.head] = write_bit
                    self.log_step(f"Sonuç alanına '{write_bit}' eklendi, sola geri dönülüyor")
                    while self.tape[self.head] != '=':
                        self.head -= 1
                    self.current_state = 'q7'
            elif self.current_state == 'q7':
                if char not in ['X', 'Y']:
                    self.head -= 1
                else:
                    self.current_state = 'q4'

        
            elif self.current_state == 'q8':
                if char != 'B':
                    if char == 'X': self.tape[self.head] = '0'
                    if char == 'Y': self.tape[self.head] = '1'
                    self.head -= 1
                else:
                    self.shift_count += 1
                    while self.tape[self.head] != '=':
                        self.head += 1
                    self.current_state = 'q9'

        
            elif self.current_state == 'q9':
                if char not in ['x', 'y', '=']:
                    self.head += 1
                else:
                    self.current_state = 'q1'
                    self.head -= 1

            elif self.current_state == 'q_clean':
                if char != '=':
                    if char == 'x': self.tape[self.head] = '0'
                    if char == 'y': self.tape[self.head] = '1'
                    self.log_step("Banttaki geçici işaretler temizleniyor, sağa hareket")
                    self.head += 1
                else:
                    
                    eq_idx = self.head
                    for k in range(len(self.tape) - eq_idx - 1):
                        self.tape[eq_idx + 1 + k] = 'B'
                    for k, bit in enumerate(correct_bin):
                        self.tape[eq_idx + 1 + k] = bit
                        
                    self.current_state = 'q_accept'
                    while self.tape[self.head] != 'B':
                        self.head += 1
                    self.head -= 1
                    self.log_step("sonuç yazıldı")

        final_str = "".join(self.tape).replace('B', '')
        result_bin = final_str.split("=")[1] if "=" in final_str else correct_bin
        if not result_bin: 
            result_bin = '0'
        result_dec = int(result_bin, 2)

        print(f"\nİşlem Sonucu:")
        print(f"Binary Sonuç: {result_bin}")
        print(f"Decimal Karşılığı: {result_dec}")

def main():
    print("--- Turing Makinesi Binary Çarpma Simülatörü ---")
    n1 = input("Birinci binary sayıyı giriniz: ")
    n2 = input("İkinci binary sayıyı giriniz: ")

    if not all(c in '01' for c in n1 + n2) or not n1 or not n2:
        print("Hata Durumu: q_reject (Girdi sadece 0 ve 1 içermelidir!)")
        return

    tm = TuringMachine(n1, n2)
    tm.run()

if __name__ == "__main__":
    main()

# Hàm chia đa thức
def poly_div(A, B):
    if B == 0: raise ZeroDivisionError
    Q, R = 0, A
    degB = B.bit_length() - 1
    while R != 0 and R.bit_length() - 1 >= degB:
        shift = (R.bit_length() - 1) - degB
        #Dịch bit
        Q ^= (1 << shift)
        R ^= (B << shift)
    return Q, R

# Hàm nhân hai đa thức
def poly_mul(A, B):
    P = 0
    while B > 0:
        if B & 1: P ^= A
        A <<= 1
        B >>= 1
    return P

# Hàm vẽ bảng
def draw_table_row(cols, widths):
    lines = [str(c).split('\n') for c in cols]
    max_lines = max(len(l) for l in lines)
    
    row_str = ""
    for i in range(max_lines):
        row_str += "| "
        for j, width in enumerate(widths):
            val = lines[j][i] if i < len(lines[j]) else ""
            row_str += f"{val:<{width}} | "
        row_str += "\n"
    return row_str

def draw_separator(widths):
    return "+" + "+".join('-' * (w + 2) for w in widths) + "+\n"


# Thuật toán tìm nghịch đảo nhân
def ext_euclid_term(A, B, a_val, b_val):
    out = ""
    out += f"\nEuclidean mở rộng cho a = {a_val}, b = {b_val} (trong GF(2^10))\n"
    out += f"m(x) tương ứng giá trị thập phân {A}\n\n"
    
    col_widths = [34, 38]
    out += draw_separator(col_widths)
    out += draw_table_row(["Calculate", "Calculate"], col_widths)
    out += draw_separator(col_widths)
    
    r_prev, r_curr = A, B
    v_prev, v_curr = 1, 0  
    w_prev, w_curr = 0, 1  
    
    # Vẽ bảng
    c1 = f"r_-1 = a = {A}"
    c3 = f"v_-1 = 1\nw_-1 = 0"
    out += draw_table_row([c1, c3], col_widths)
    out += draw_separator(col_widths)
    
    c1 = f"r_0 = b = {B}"
    c3 = f"v_0 = 0\nw_0 = 1"
    out += draw_table_row([c1, c3], col_widths)
    out += draw_separator(col_widths)
    
    step = 1
    while True:
        q, r_next = poly_div(r_prev, r_curr)
        
        if r_next == 0:
            c1 = f"r_{step} = r_{step-2} mod r_{step-1}\n     = {r_prev} mod {r_curr} = 0\nq_{step} = {r_prev} / {r_curr} = {q}"
            c3 = f"GCD = r_{step-1} = {r_curr}"
            inv_val = ""
            if r_curr == 1:
                c3 += f"\n=> Nghịch đảo nhân là w_{step-1} = {w_curr}"
                inv_val = str(w_curr)
            else:
                inv_val = "không tồn tại"
            
            out += draw_table_row([c1, c3], col_widths)
            out += draw_separator(col_widths)
            break
            
        v_next = v_prev ^ poly_mul(q, v_curr)
        w_next = w_prev ^ poly_mul(q, w_curr)
        
        c1 = f"r_{step} = r_{step-2} mod r_{step-1}\n     = {r_prev} mod {r_curr} = {r_next}\nq_{step} = {r_prev} / {r_curr} = {q}"
        c3 = f"v_{step} = v_{step-2} - q_{step}*v_{step-1}\n     = {v_prev} ^ ({q}*{v_curr}) = {v_next}\nw_{step} = w_{step-2} - q_{step}*w_{step-1}\n     = {w_prev} ^ ({q}*{w_curr}) = {w_next}"
        
        out += draw_table_row([c1, c3], col_widths)
        out += draw_separator(col_widths)
        
        r_prev, r_curr = r_curr, r_next
        v_prev, v_curr = v_curr, v_next
        w_prev, w_curr = w_curr, w_next
        step += 1
        
    return out, inv_val
#Hàm main
if __name__ == '__main__':
    m = (1 << 10) | (1 << 3) | 1 
    
    print("--- Thuật toán Extended Euclidean trong GF(2^10) ---")
    print("Đa thức tối giản mặc định m(x) = x^10 + x^3 + 1 (giá trị: 1033)")
    a_in = input("Nhập vào giá trị a: ")
    b_in = input("Nhập vào giá trị b: ")
    
    try:
        a = int(a_in)
        b = int(b_in)
    except ValueError:
        print("Vui lòng nhập một số nguyen hợp lệ. Thoát chương trình.")
        exit(1)
        
    out_a, inv_a = ext_euclid_term(m, a, "m(x)", str(a))
    out_b, inv_b = ext_euclid_term(m, b, "m(x)", str(b))
    
    print(out_a)
    print(out_b)
    print(f"Kết luận: Vậy, nghịch đảo của {a} là {inv_a}, nghịch đảo của {b} là {inv_b}.")

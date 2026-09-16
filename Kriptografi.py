def decrypt_enigma(ciphertext):
    # Konfigurasi Rotor (Standard Enigma I)
    rotors = {
        'I': 'EKMFLGDQVZNTOWYHXUSPAIBRCJ',
        'II': 'AJDKSIRUXBLHWTMCQGZNPYFVOE',
        'III': 'BDFHJLCPRTXVZNYEIWGAKMUSQO'
    }
    reflector_b = 'YRUHQSLDPXNGOKMIEBFZCWVJAT'
    turnovers = {'I': 'Q', 'II': 'E', 'III': 'V'}

    # Setting Kanan ke Kiri (I, II, III)
    # Posisi awal (kanan ke kiri): E, B, M -> (4, 1, 12)
    pos = [4, 1, 12] 
    
    # Ring setting (kanan ke kiri): F, U, T -> (5, 20, 19)
    rings = [5, 20, 19]

    # Plugboard
    plugboard = {'A':'U', 'U':'A', 'D':'L', 'L':'D'}

    def step_rotors():
        step_mid = False
        step_left = False
        
        # Enigma double-stepping mechanism
        if chr(pos[1] + 65) == turnovers['II']:
            step_mid = True
            step_left = True
        elif chr(pos[0] + 65) == turnovers['I']:
            step_mid = True

        pos[0] = (pos[0] + 1) % 26
        if step_mid:
            pos[1] = (pos[1] + 1) % 26
        if step_left:
            pos[2] = (pos[2] + 1) % 26

    plaintext = ""
    for char in ciphertext:
        step_rotors()
        
        # Melewati Plugboard
        c = plugboard.get(char, char)
        c_idx = ord(c) - 65

        # Sinyal Maju: Kanan (I) -> Tengah (II) -> Kiri (III)
        for i in range(3):
            offset = (pos[i] - rings[i]) % 26
            in_idx = (c_idx + offset) % 26
            
            if i == 0: wiring = rotors['I']
            elif i == 1: wiring = rotors['II']
            else: wiring = rotors['III']
            
            out_char = wiring[in_idx]
            c_idx = (ord(out_char) - 65 - offset) % 26

        # Reflector B
        c_idx = ord(reflector_b[c_idx]) - 65

        # Sinyal Mundur: Kiri (III) -> Tengah (II) -> Kanan (I)
        for i in range(2, -1, -1):
            offset = (pos[i] - rings[i]) % 26
            in_idx = (c_idx + offset) % 26
            in_char = chr(in_idx + 65)
            
            if i == 0: wiring = rotors['I']
            elif i == 1: wiring = rotors['II']
            else: wiring = rotors['III']
            
            out_idx = wiring.index(in_char)
            c_idx = (out_idx - offset) % 26

        # Melewati Plugboard (Kembali)
        out_char = chr(c_idx + 65)
        out_char = plugboard.get(out_char, out_char)
        plaintext += out_char
        
    return plaintext

# Jalankan fungsi
ciphertext = "CVVFFOKLVNYOGVECAPBVPALVSLKUMXQAISLAAM"
print("Plaintext Bagian 3:", decrypt_enigma(ciphertext))
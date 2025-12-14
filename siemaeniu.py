import streamlit as st

# Tytuł aplikacji
st.title("📦 Prosty Magazyn")

# --- Inicjalizacja listy w pamięci podręcznej (Session State) ---
# Jest to konieczne w Streamlit, aby lista nie czyściła się przy każdym kliknięciu.
if 'towary' not in st.session_state:
    st.session_state.towary = []

# --- Sekcja dodawania towaru ---
st.header("Dodaj nowy towar")

with st.form("dodawanie_form"):
    # Pole tekstowe na nazwę towaru
    nowy_towar = st.text_input("Nazwa produktu")
    # Możliwość określenia ilości przy dodawaniu
    ilosc = st.number_input("Ilość", min_value=1, value=1, step=1)
    
    # Przycisk zatwierdzający formularz
    submit_button = st.form_submit_button("Dodaj do magazynu")

    if submit_button:
        if nowy_towar:
            nowy_towar = nowy_towar.strip() # Usuwamy zbędne spacje
            znaleziono = False
            
            # Sprawdzamy czy towar już jest na liście
            for towar in st.session_state.towary:
                # Jeśli nazwy są takie same (ignorując wielkość liter dla wygody)
                if towar['nazwa'].lower() == nowy_towar.lower():
                    towar['ilosc'] += ilosc
                    st.success(f"Zaktualizowano ilość: {towar['nazwa']} (Razem: {towar['ilosc']})")
                    znaleziono = True
                    break
            
            # Jeśli nie znaleziono, dodajemy nowy wpis (słownik z nazwą i ilością)
            if not znaleziono:
                st.session_state.towary.append({'nazwa': nowy_towar, 'ilosc': ilosc})
                st.success(f"Dodano nowy produkt: {nowy_towar}")
        else:
            st.warning("Proszę wpisać nazwę towaru.")

# --- Sekcja wyświetlania i usuwania towarów ---
st.header("Stan magazynowy")

# Sprawdzenie czy magazyn jest pusty
if not st.session_state.towary:
    st.info("Magazyn jest pusty.")
else:
    # Wyświetlenie listy towarów
    for i, towar in enumerate(st.session_state.towary):
        col1, col2, col3 = st.columns([3, 2, 1])
        
        # Kolumna z nazwą towaru
        # Teraz odwołujemy się do pola 'nazwa' w słowniku
        col1.write(f"**{i + 1}.** {towar['nazwa']}")
        
        # Kolumna z ilością
        col2.write(f"Ilość: {towar['ilosc']} szt.")
        
        # Kolumna z przyciskiem usuwania
        # Używamy unikalnego klucza (key) dla każdego przycisku
        if col3.button("Usuń", key=f"usun_{i}"):
            st.session_state.towary.pop(i)
            st.rerun() # Odświeżenie aplikacji po usunięciu

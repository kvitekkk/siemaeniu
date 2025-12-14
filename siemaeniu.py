import streamlit as st

# Tytuł aplikacji
st.title("📦 Prosty Magazyn")

# --- Inicjalizacja listy w pamięci podręcznej (Session State) ---
# Jest to konieczne w Streamlit, aby lista nie czyściła się przy każdym kliknięciu.
if 'towary' not in st.session_state:
    st.session_state.towary = []

# --- Sekcja 1: Dodawanie towaru (Przyjęcie) ---
st.header("1. Przyjęcie towaru (Dodaj)")

with st.form("dodawanie_form"):
    # Pole tekstowe na nazwę towaru
    nowy_towar = st.text_input("Nazwa produktu")
    # Możliwość określenia ilości przy dodawaniu
    ilosc = st.number_input("Ilość do dodania", min_value=1, value=1, step=1)
    
    # Przycisk zatwierdzający formularz
    submit_dodaj = st.form_submit_button("Dodaj do magazynu")

    if submit_dodaj:
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

# --- Sekcja 2: Wydawanie towaru (Usuwanie/Zmniejszanie) ---
st.header("2. Wydanie towaru (Zdejmij)")

if st.session_state.towary:
    with st.form("usuwanie_form"):
        # Tworzymy listę nazw produktów do wyboru w liście rozwijanej
        opcje_produktow = [t['nazwa'] for t in st.session_state.towary]
        wybrany_produkt = st.selectbox("Wybierz produkt do wydania", opcje_produktow)
        
        ilosc_usun = st.number_input("Ilość do wydania/usunięcia", min_value=1, value=1, step=1)
        submit_usun = st.form_submit_button("Zdejmij ze stanu")
        
        if submit_usun:
            for i, towar in enumerate(st.session_state.towary):
                if towar['nazwa'] == wybrany_produkt:
                    if towar['ilosc'] > ilosc_usun:
                        towar['ilosc'] -= ilosc_usun
                        st.success(f"Wydano {ilosc_usun} szt. produktu {wybrany_produkt}. Pozostało: {towar['ilosc']}")
                    elif towar['ilosc'] == ilosc_usun:
                        st.session_state.towary.pop(i)
                        st.warning(f"Produkt {wybrany_produkt} został całkowicie wyprzedany i usunięty z listy.")
                    else:
                        st.error(f"Błąd! Próbujesz usunąć {ilosc_usun}, a w magazynie jest tylko {towar['ilosc']}.")
                    st.rerun() # Odświeżamy aplikację, aby zaktualizować tabelę poniżej
                    break
else:
    st.info("Brak towarów do wydania.")

# --- Sekcja 3: Wyświetlanie stanu magazynowego ---
st.header("3. Aktualny stan magazynowy")

# Sprawdzenie czy magazyn jest pusty
if not st.session_state.towary:
    st.info("Magazyn jest pusty.")
else:
    # Wyświetlenie listy towarów
    for i, towar in enumerate(st.session_state.towary):
        col1, col2, col3 = st.columns([3, 2, 2])
        
        # Kolumna z nazwą towaru
        col1.write(f"**{i + 1}.** {towar['nazwa']}")
        
        # Kolumna z ilością
        col2.write(f"Ilość: {towar['ilosc']} szt.")
        
        # Kolumna z przyciskiem szybkiego usuwania (cały wiersz)
        if col3.button("Usuń całkowicie", key=f"usun_calosc_{i}"):
            st.session_state.towary.pop(i)
            st.rerun()

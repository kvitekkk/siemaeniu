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
    # Przycisk zatwierdzający formularz
    submit_button = st.form_submit_button("Dodaj do magazynu")

    if submit_button:
        if nowy_towar:
            # Dodanie towaru do listy
            st.session_state.towary.append(nowy_towar)
            st.success(f"Dodano produkt: {nowy_towar}")
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
        col1, col2 = st.columns([4, 1])
        
        # Kolumna z nazwą towaru
        col1.write(f"**{i + 1}.** {towar}")
        
        # Kolumna z przyciskiem usuwania
        # Używamy unikalnego klucza (key) dla każdego przycisku
        if col2.button("Usuń", key=f"usun_{i}"):
            st.session_state.towary.pop(i)
            st.rerun() # Odświeżenie aplikacji po usunięciu

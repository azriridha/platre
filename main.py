import streamlit as st
import json
from PIL import Image
import os
import base64
from streamlit_carousel import carousel  # 🔁 À mettre en haut de ton fichier


st.set_page_config(page_title="Vitrine 3D", layout="wide")
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_png_as_page_bg(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{bin_str}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        background-position: center;
    }}
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)

# ✅ Appel de la fonction
#set_png_as_page_bg("images/rosier.png")







# Charger produits
with open("data/produits.json", "r") as f:
    produits = json.load(f)

# Initialisation des états
if "page" not in st.session_state:
    st.session_state.page = "Accueil"

if "produit_selectionne" not in st.session_state:
    st.session_state.produit_selectionne = None

if "image_selectionnee" not in st.session_state:
    st.session_state.image_selectionnee = None
# Liste des options valides
menu_options = ["Accueil", "Nos Produits", "Contact"]

# Lecture sécurisée des paramètres
query_params = st.query_params
default_menu = query_params.get("menu", ["Accueil"])[0]
if default_menu not in menu_options:
    default_menu = "Accueil"

menu = st.sidebar.radio("Navigation", menu_options, index=menu_options.index(default_menu))

# Mise à jour de la page uniquement depuis le menu, sauf si on est déjà dans la fiche produit
if st.session_state.get("page") != "fiche":
    if menu == "Nos Produits":
        st.session_state.page = "liste"
    else:
        st.session_state.page = menu





# --- PAGE ACCUEIL ---
if st.session_state.page == "Accueil":
    if st.session_state.page == "Accueil":
        st.title("✨ Bienvenue sur Bloom")
        st.subheader("Votre vitrine de panneaux décoratifs 3D en plâtre")

        st.write("""
        🎨 **Sublimez vos murs avec élégance et créativité**.  
        Nos panneaux en plâtre 3D transforment vos espaces intérieurs avec style, volume et personnalité.

        🛠️ Fabriqués avec soin en Tunisie, nos produits allient design contemporain et qualité artisanale.

        👉 Explorez notre collection exclusive dans l'onglet **Nos Produits** ou contactez-nous pour un devis personnalisé.
        """)

        # Illustration ou bannière
        st.image("images/bg.png", use_container_width=True, caption="Design mural 3D – rendu élégant")

        if st.button("🔎 Voir nos produits"):
            st.session_state.page = "liste"
            st.rerun()

    st.markdown("---")
    st.subheader("📱 Suivez-nous sur les réseaux sociaux")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""
            <a href="https://facebook.com/tonpage" target="_blank">
                <img src="https://img.icons8.com/fluency/48/000000/facebook-new.png"/>
            </a>
            """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <a href="https://instagram.com/tonprofil" target="_blank">
                <img src="https://img.icons8.com/fluency/48/000000/instagram-new.png"/>
            </a>
            """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
            <a href="https://wa.me/216XXXXXXXX" target="_blank">
                <img src="https://img.icons8.com/fluency/48/000000/whatsapp.png"/>
            </a>
            """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
            <a href="mailto:contact@tonsite.com">
                <img src="https://img.icons8.com/fluency/48/000000/email-open.png"/>
            </a>
            """, unsafe_allow_html=True)

# --- PAGE LISTE DES PRODUITS ---
elif st.session_state.page == "liste":
    st.title("🧱 Nos Panneaux 3D en Plâtre")

    produits_par_page = 6
    total_pages = (len(produits) - 1) // produits_par_page + 1
    page_actuelle = st.number_input("Page", min_value=1, max_value=total_pages, value=1, step=1)

    start = (page_actuelle - 1) * produits_par_page
    end = start + produits_par_page
    produits_affiches = produits[start:end]

    rows = [produits_affiches[i:i + 3] for i in range(0, len(produits_affiches), 3)]

    for index_global, row in enumerate(rows):
        cols = st.columns(3)
        for i, produit in enumerate(row):
            with cols[i]:
                produit_index = start + (index_global * 3) + i
                try:
                    image_path = os.path.join("images", produit["images"][0])
                    image = Image.open(image_path)

                    # Redimensionnement uniforme (300x300)
                    target_size = (300, 300)
                    image.thumbnail(target_size, Image.Resampling.LANCZOS)
                    bg = Image.new("RGB", target_size, (255, 255, 255))
                    offset = ((target_size[0] - image.width) // 2, (target_size[1] - image.height) // 2)
                    bg.paste(image, offset)

                    st.image(bg, use_container_width=False)
                except:
                    st.warning("Image manquante")

                st.subheader(produit["nom"])
                st.markdown(f"**Prix :** {produit['prix']}")
                st.markdown(f"**description :** {produit['description']}")
                if st.button("Voir ce produit", key=f"voir_{produit_index}"):
                    st.session_state.produit_selectionne = produit
                    st.session_state.image_selectionnee = produit["images"][0]
                    st.session_state.page = "fiche"
                    st.rerun()

# --- PAGE FICHE PRODUIT ---
# elif st.session_state.page == "fiche":
#     produit = st.session_state.produit_selectionne
#     if produit:
#         st.button("⬅️ Retour à la liste", on_click=lambda: st.session_state.update({"page": "liste"}))
#         st.title(produit["nom"])
#
#         # Image principale
#         try:
#             image_path = os.path.join("images", st.session_state.image_selectionnee)
#             image = Image.open(image_path)
#             st.image(image, use_container_width=False, caption="Aperçu")
#         except:
#             st.error("Image principale non disponible")
#
#         # Miniatures façon galerie
#         st.write("### Galerie")
#         mini_cols = st.columns(len(produit["images"]))
#         thumb_size = (300, 300)
#
#         for i, img_name in enumerate(produit["images"]):
#             with mini_cols[i]:
#                 if st.button(" ", key=f"miniature_{i}"):
#                     st.session_state.image_selectionnee = img_name
#                     st.rerun()
#                 try:
#                     img_path = os.path.join("images", img_name)
#                     img = Image.open(img_path)
#                     img.thumbnail(thumb_size, Image.Resampling.LANCZOS)
#                     thumb_bg = Image.new("RGB", thumb_size, (255, 255, 255))
#                     offset = ((thumb_size[0] - img.width) // 2, (thumb_size[1] - img.height) // 2)
#                     thumb_bg.paste(img, offset)
#                     st.image(thumb_bg)
#                 except:
#                     st.warning("Image non trouvée")
#
#         st.markdown(f"### 💰 Prix : {produit['prix']}")
#         st.markdown("### 📝 Description :")
#         st.write(produit["description"])
#
#         couleur = st.selectbox("🎨 Choisissez une couleur", ["Blanc", "Gris", "Beige", "Personnalisée"])
#         message = st.text_area("✉️ Votre demande (dimensions, quantité...)")
#
#         if st.button("📩 Envoyer la demande"):
#             st.success("Votre demande a été envoyée avec succès ✅")

# --- PAGE CONTACT ---



elif st.session_state.page == "fiche":
    produit = st.session_state.produit_selectionne
    if produit:
        st.button("⬅️ Retour à la liste", on_click=lambda: st.session_state.update({"page": "liste"}))
        st.title(produit["nom"])

        # # Image principale (optionnelle si on affiche aussi dans le carrousel)
        # try:
        #     image_path = os.path.join("images", st.session_state.image_selectionnee)
        #     image = Image.open(image_path)
        #     st.image(image, use_container_width=False, caption="Aperçu")
        # except:
        #     st.error("Image principale non disponible")

        # ✅ Galerie en carrousel
        st.subheader("🎞️ Galerie du produit")
        carrousel_items = []

        for img_name in produit["images"]:
            img_path = os.path.join("images", img_name)
            # Ajout d’un item à la liste du carrousel
            carrousel_items.append({
                "title": produit["nom"],
                "text": produit["description"][:80] + "...",
                "img": img_path
            })

        # Affichage du carrousel
        if carrousel_items:
            carousel(items=carrousel_items)

        # Détails produit
        st.markdown(f"### 💰 Prix : {produit['prix']}")
        st.markdown("### 📝 Description :")
        st.write(produit["description"])

        couleur = st.selectbox("🎨 Choisissez une couleur", ["Blanc", "Gris", "Beige", "Personnalisée"])
        quantity = st.number_input("Quantité", min_value=0, step=1, value=1, format="%d")
        st.success(f"Nombre de m² sélectionné: {quantity}")
        st.success(f"Nombre de panneaux: {quantity * 4}")
        st.success(f"Soit un total de: {float(produit['prix']) * quantity} DTN")
        message = st.text_area("✉️ Votre demande (commentaire et remarques...)")

        if st.button("📩 Envoyer la demande"):
            st.success("Votre demande a été envoyée avec succès ✅")

elif st.session_state.page == "Contact":
    st.title("📞 Contactez-nous")
    st.write("Vous avez une question ? Remplissez le formulaire ci-dessous :")

    nom = st.text_input("Nom")
    email = st.text_input("Email")
    telephone = st.text_input("Téléphone")
    message = st.text_area("Message")

    if st.button("Envoyer"):
        if nom and email and message:
            st.success("Message envoyé avec succès ✅")
        else:
            st.error("Veuillez remplir tous les champs.")

    st.markdown("---")
    st.subheader("📱 Suivez-nous sur les réseaux sociaux")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""
        <a href="https://facebook.com/tonpage" target="_blank">
            <img src="https://img.icons8.com/fluency/48/000000/facebook-new.png"/>
        </a>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <a href="https://instagram.com/tonprofil" target="_blank">
            <img src="https://img.icons8.com/fluency/48/000000/instagram-new.png"/>
        </a>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <a href="https://wa.me/216XXXXXXXX" target="_blank">
            <img src="https://img.icons8.com/fluency/48/000000/whatsapp.png"/>
        </a>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <a href="mailto:contact@tonsite.com">
            <img src="https://img.icons8.com/fluency/48/000000/email-open.png"/>
        </a>
        """, unsafe_allow_html=True)

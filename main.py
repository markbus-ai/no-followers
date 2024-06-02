import instaloader
from instaloader.exceptions import TwoFactorAuthRequiredException
import flet as ft

def main(page: ft.Page):
    usuario = ft.TextField(label="Username", text_align="LEFT")
    contraseña = ft.TextField(label="Password", password=True, can_reveal_password=True, text_align="LEFT")
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def non_followers(e):
        username = usuario.value
        password = contraseña.value

        # Crea una instancia de Instaloader
        L = instaloader.Instaloader()
        
        try:
            # Intenta iniciar sesión en Instagram
            L.login(username, password)
        except TwoFactorAuthRequiredException:
            # Si se requiere autenticación de dos factores, solicita el código de verificación
            verification_code_field = ft.TextField(label="Enter verification code")
            dialog = ft.AlertDialog(
                title=ft.Text("Two-Factor Authentication Required"),
                content=verification_code_field,
                actions=[ft.TextButton("OK", on_click=lambda _: page.dialog.close())]
            )
            page.dialog = dialog
            dialog.open = True
            page.update()
            return

        # Obtiene el perfil del usuario
        profile = instaloader.Profile.from_username(L.context, username)

        # Obtiene los seguidores del usuario
        followers = set(profile.get_followers())

        # Obtiene las personas que sigue el usuario
        following = set(profile.get_followees())

        # Encuentra quién no te sigue de vuelta
        not_following_back = following - followers

        # Muestra los usuarios que no te siguen de vuelta en la interfaz de Flet
        resultados = ft.ListView(expand=True, spacing=10)
        for user in not_following_back:
            resultados.controls.append(ft.Text(f"{user.username} no te sigue"))
        
        # Limpiar la página y agregar los nuevos elementos
        page.controls.clear()
        page.add(usuario, contraseña, ft.TextButton(text="Submit", on_click=non_followers), resultados)
        page.update()

    page.add(usuario, contraseña, ft.TextButton(text="Submit", on_click=non_followers))

ft.app(target=main)

from flet import *
import os


def main(page: Page):
    page.title = "Planeja Plant."

    def window_event(e):
        if e.data == "close":
            page.dialog = confirmacao_saida
            confirmacao_saida.open = True
            page.update()

    def page_resize(e):
        page.update()

    page.on_resize = page_resize
    page.window_prevent_close = True
    page.window_maximized = True
    page.window_min_width = 800
    page.window_min_height = 600
    page.vertical_alignment = MainAxisAlignment.END
    page.horizontal_alignment = CrossAxisAlignment.END
    page.on_window_event = window_event
    page.theme_mode = ThemeMode.LIGHT
    page.window_center()

    def drag_will_accept(e):
        e.control.content.border = border.all(
            2, colors.BLACK45 if e.data == "true" else colors.RED
        )
        e.control.update()

    def atualizar_lista_frutas(e):
        for fila in ["A", "B", "C", "D", "E"]:
            for numero in range(1, 11):
                print(fila, numero)

    def drag_accept(e: DragTargetAcceptEvent):
        src = page.get_control(e.src_id)
        e.control.content.bgcolor = src.content.bgcolor
        e.control.content.image_src = src.content.image_src
        e.control.content.content = src.content.content
        e.control.content.image_fit = src.content.image_fit

        e.control.content.border = None
        e.control.update()

    def drag_leave(e):
        e.control.content.border = None
        e.control.update()

    def nao_click(e):
        confirmacao_saida.open = False
        page.update()

    arquivos_imagens_frutas = os.listdir("FRUTAS")

    confirmacao_saida = AlertDialog(
        modal=True,
        title=Text(
            value="CONFIRMAR SAIDA?",
            weight=FontWeight.BOLD,
            color=colors.RED,
            italic=True,
            text_align=TextAlign.CENTER,
        ),
        content=Text(
            value="DESEJA REALMENTE SAIR?\nQUALQUE ALTERAÇÃO NÃO SALVA SERÁ PERDIDA!",
            weight=FontWeight.BOLD,
            color=colors.BLACK,
        ),
        actions=[
            ElevatedButton(
                text="SIM",
                on_click=lambda _: page.window_destroy(),
                icon=icons.CHECK,
                icon_color=colors.GREEN,
                bgcolor=colors.GREEN_50,
                style=ButtonStyle(
                    side={
                        MaterialState.DEFAULT: BorderSide(1, colors.GREEN),
                        MaterialState.HOVERED: BorderSide(2, colors.BLACK),
                    },
                    shape={
                        MaterialState.DEFAULT: RoundedRectangleBorder(radius=2),
                        MaterialState.HOVERED: RoundedRectangleBorder(radius=20),
                    },
                ),
            ),
            ElevatedButton(
                text="NÃO",
                on_click=nao_click,
                icon=icons.CANCEL,
                icon_color=colors.RED,
                bgcolor=colors.RED_50,
                autofocus=True,
                style=ButtonStyle(
                    side={
                        MaterialState.DEFAULT: BorderSide(1, colors.RED),
                        MaterialState.HOVERED: BorderSide(2, colors.BLACK),
                    },
                    shape={
                        MaterialState.DEFAULT: RoundedRectangleBorder(radius=2),
                        MaterialState.HOVERED: RoundedRectangleBorder(radius=20),
                    },
                ),
            ),
        ],
        actions_alignment=MainAxisAlignment.END,
        alignment=alignment.center,
    )
    lista_frutas = ListView(
        expand=1,
        spacing=10,
        padding=10,
        width=page.window_width * 0.2,
        controls=[
            Draggable(
                content=Container(
                    content=Text(
                        value=str(fruta.split(".")[0]),
                        text_align=TextAlign.CENTER,
                        weight=FontWeight.BOLD,
                        color=colors.WHITE,
                        bgcolor=colors.BLACK,
                    ),
                    image_src=f"FRUTAS/{fruta}",
                    image_fit=ImageFit.FILL,
                    bgcolor=colors.BLUE_200,
                    border_radius=5,
                    alignment=alignment.top_center,
                    width=200,
                    height=200,
                ),
                content_feedback=Container(
                    content=Text(
                        value=str(fruta.split(".")[0]),
                        size=20,
                        text_align=TextAlign.CENTER,
                        weight=FontWeight.BOLD,
                        color=colors.WHITE,
                        bgcolor=colors.BLACK,
                    ),
                    image_src=f"FRUTAS/{fruta}",
                    image_fit=ImageFit.FILL,
                    bgcolor=colors.BLUE_200,
                    border_radius=5,
                    alignment=alignment.top_center,
                    width=100,
                    height=100,
                    opacity=0.8,
                ),
            ) for fruta in sorted(os.listdir("FRUTAS"))
        ]
    )
    area_plantio = GridView(
        expand=1,
        runs_count=8,
        controls=[
            DragTarget(
                content=Container(
                    content=Text(f"A-{x}"),
                    key=f"A-{x}",
                    bgcolor=colors.GREEN_400,
                    border_radius=5,
                    expand=1,
                    alignment=alignment.center,
                    width=50,
                    height=50,
                ),
                on_will_accept=drag_will_accept,
                on_accept=drag_accept,
                on_leave=drag_leave,
            ) for x in range(1, 101)
        ],
    )

    def route_change(route):
        page.views.clear()
        page.views.append(
            View(
                route="/",
                controls=[
                    AppBar(
                        title=Text(
                            value="PLANEJAMENTO",
                            weight=FontWeight.BOLD,
                            color=colors.BLACK,
                            text_align=TextAlign.CENTER,
                            size=45,
                        ),
                        actions=[
                            IconButton(
                                icon=icons.REFRESH,
                                icon_color=colors.BLACK,
                                bgcolor=colors.WHITE,
                                tooltip="ATUALIZAR PÁGINA",
                                on_click=atualizar_lista_frutas
                            )
                        ],
                        bgcolor=colors.LIGHT_GREEN_300,
                        center_title=True,
                    ),
                    Row(
                        controls=[
                            Column(
                                controls=[
                                    Container(
                                        content=Text(
                                            value="SELECIONE UMA PLANTA",
                                            size=20,
                                            text_align=TextAlign.CENTER,
                                            weight=FontWeight.BOLD,
                                            color=colors.BLACK,
                                        ),
                                        bgcolor=colors.BLUE_200,
                                        border_radius=5,
                                        shadow=BoxShadow(
                                            spread_radius=1,
                                            blur_radius=10,
                                            color=colors.BLUE_100,
                                            offset=Offset(0, 0),
                                            blur_style=ShadowBlurStyle.OUTER,
                                        ),
                                    ),
                                    lista_frutas,
                                ],
                                expand=1,
                                alignment=MainAxisAlignment.CENTER,
                                horizontal_alignment=CrossAxisAlignment.CENTER,
                            ),
                            area_plantio,
                        ],
                        expand=1,
                        width=page.window_width * 0.90,
                        alignment=MainAxisAlignment.CENTER,
                        vertical_alignment=CrossAxisAlignment.CENTER,
                    ),
                ],
            )
        )

        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)


app(target=main)

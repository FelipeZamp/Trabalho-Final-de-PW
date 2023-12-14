from fastapi import (
    APIRouter,
    Depends,
    Form,
    HTTPException,
    Path,
    Request,
    status,
)
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from models.Usuario import Usuario
from repositories.UsuarioRepo import UsuarioRepo
from util.mensagem import redirecionar_com_mensagem
from util.seguranca import conferir_senha, obter_hash_senha, obter_usuario_logado

router = APIRouter(prefix="/usuario")
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def get_index(
    request: Request,
    usuario: Usuario = Depends(obter_usuario_logado),
):
    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if not usuario.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    
    usuarios = UsuarioRepo.obter_todos()
    
    return templates.TemplateResponse(
        "usuario/index.html",
        {"request": request, "usuario": usuario, "usuarios": usuarios},
    )

@router.get("/excluir/{id_usuario:int}", response_class=HTMLResponse)
async def get_excluir(
    request: Request,
    id_usuario: int = Path(),
    usuario: Usuario = Depends(obter_usuario_logado),
):
    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if not usuario.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    usuario_excluir = UsuarioRepo.obter_por_id(id_usuario)
    
    return templates.TemplateResponse(
        "usuario/excluir.html",
        {"request": request, "usuario": usuario, "usuario_excluir": usuario_excluir},
    )

@router.post("/excluir/{id_usuario:int}", response_class=HTMLResponse)
async def post_excluir(
    usuario: Usuario = Depends(obter_usuario_logado),
    id_usuario: int = Path(),
):
    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if not usuario.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    
    if id_usuario == 1:
        response = redirecionar_com_mensagem(
            "/usuario",
            "Não é possível excluir o administrador padrão do sistema.",
        )
        return response
    
    if id_usuario == usuario.id:
        response = redirecionar_com_mensagem(
            "/usuario",
            "Não é possível excluir o próprio usuário que está logado.",
        )
        return response
    
    UsuarioRepo.excluir(id_usuario)
    response = redirecionar_com_mensagem(
        "/usuario",
        "Usuário excluído com sucesso.",
    )
    return response

@router.get("/alterar/{id_usuario:int}", response_class=HTMLResponse)
async def get_alterar(
    request: Request,
    id_usuario: int = Path(),
    usuario: Usuario = Depends(obter_usuario_logado),
):
    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if not usuario.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    
    usuario_alterar = UsuarioRepo.obter_por_id(id_usuario)
    
    return templates.TemplateResponse(
        "usuario/alterar.html",
        {"request": request, "usuario": usuario, "usuario_alterar": usuario_alterar},
    )

@router.post("/alterar/{id_usuario:int}", response_class=HTMLResponse)
async def post_alterar(
    id_usuario: int = Path(),
    nome: str = Form(...),
    email: str = Form(...),
    administrador: bool = Form(False),
    usuario: Usuario = Depends(obter_usuario_logado),
):
    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if not usuario.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    
    if id_usuario == 1:
        response = redirecionar_com_mensagem(
            "/usuario",
            "Não é possível alterar dados do administrador padrão.",
        )
        return response
    
    UsuarioRepo.alterar(
        Usuario(id=id_usuario, nome=nome, email=email, admin=administrador)
    )
    
    response = redirecionar_com_mensagem(
        "/usuario",
        "Usuário alterado com sucesso.",
    )
    
    return response

@router.get("/inserir")
async def get_inserir(request: Request,):
    return templates.TemplateResponse("/usuario/inserir.html", {"request": request},)

@router.post("/inserir", response_class=HTMLResponse)
async def post_inserir(
    senha: str = Form(...),
    confirmar: str = Form(...),
    nome: str = Form(...), 
    email: str = Form(...), 
    administrador: bool = Form(False), 
    usuario: Usuario = Depends(obter_usuario_logado)):

    verificarEmail = UsuarioRepo.existe_email(email)

    if verificarEmail == 1:
        response = redirecionar_com_mensagem("/usuario/inserir", "Email Inválido!")
        return response           

    if senha == confirmar:
        hash = obter_hash_senha(senha)

        usuario = Usuario(nome=nome, email=email, senha=hash, admin=administrador)
        UsuarioRepo.inserir(usuario)
        response = redirecionar_com_mensagem("/login", "Usuario criado com sucesso! Entre com seu email e senha para acessar!")
        return response
    else:
        response = redirecionar_com_mensagem("/usuario/inserir", "As senhas não são iguais!")
        return response
    

@router.get("/arearestrita", response_class=HTMLResponse)
async def get_area_restrita(
    request: Request,
    usuario: Usuario = Depends(obter_usuario_logado),):

    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    return templates.TemplateResponse("usuario/arearestrita.html", {"request": request, "usuario": usuario},)

@router.post("/alterardados", response_class=HTMLResponse)
async def post_alterarDados(
    nome: str = Form(...),
    email: str = Form(...),
    administrador: bool = Form(False),
    usuario: Usuario = Depends(obter_usuario_logado),
    ):

    senhaCadastrada = UsuarioRepo.obter_senha_por_email(usuario.email)

    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if usuario.id == 1:
        response = redirecionar_com_mensagem("/usuario/arearestrita", "Não é possível alterar dados do administrador padrão.",)
        return response
    
    user = Usuario(nome=nome, email=email,senha=senhaCadastrada,admin=administrador,id=usuario.id)
    print(user)
    UsuarioRepo.alterar(user)

    response = redirecionar_com_mensagem("/usuario/arearestrita", "Usuário alterado com sucesso.",)   
    return response
    
@router.post("/alterarsenha", response_class=HTMLResponse)
async def post_alteraSenha(
    senhaAtual: str = Form(...),
    novaSenha: str = Form(...),
    confirmarSenha: str = Form(...),
    usuario: Usuario = Depends(obter_usuario_logado)
    ):

    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    senhaCadastrada = UsuarioRepo.obter_senha_por_email(usuario.email)

    if conferir_senha(senhaAtual, senhaCadastrada):
        if novaSenha == confirmarSenha:
            hashNovaSenha = obter_hash_senha(novaSenha)
            user = Usuario(nome=usuario.nome, email=usuario.email,senha=hashNovaSenha,admin=usuario.admin,id=usuario.id)
            UsuarioRepo.alterar(user)
            response = redirecionar_com_mensagem("/usuario/arearestrita", "Senha alterada com sucesso")
        else:
            response = redirecionar_com_mensagem("/usuario/arearestrita", "As senhas não coincidem!")
    else:
        response = redirecionar_com_mensagem("/usuario/arearestrita", "Informe a senha atual corretamente!")
    return response
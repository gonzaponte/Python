#Amosar texto ou datos por pantalla:
print texto, datos
print 'texto %f, %s' % (3, '=)' ) -> texto 3.0, =)

#Adquirir texto ou datos por pantalla:
variable = input('mensaxe para amosar: ')

#Tipos de datos:
3 = enteiro
3L = long
3.3 = 0.33e1 = float ou double
3 + 3j = complexo
'3a' ou "a3" = strings
True / False = booleanos
04 = octal
0x4 = hexadecimal

#convertir entre tipos:
float(3) = 3.0
int( 3.3 ) = 3
int( '123' ) = 123

#Operacións:
+ sumar
- restar
* multiplicar
** exponenciar
/  dividir # coidado ao dividir enteiros! 7/2 = 3 -> 7.0/2 = 7/2.0 = 3.5
// división enteira # 3.9//2 = 1.0
% módulo # dá o resto: 7 % 2 = 1

#Saber de que tipo é unha variable:
type(variable) #devolve unha variable tipo type

#Saber se unha variable é dun tipo concreto:
isinstante( variable, tipo ) p.ex. ( 3, double ) #devolve False

#Strings:
unicode: a = u'bla'
raw:     a = r'bla' #escribe tal cual (non interpreta opcións de texto)
'hola'+' '+'mundo' = 'hola mundo'
'aeiou'*3='aeiouaeiouaeiou'

Métodos:
.count( subcadea, comezo=0, final= len(cadea) ) = conta o número de veces que aparece a subcadea dende comezo ata final
.find( subcadea, comezo=0, final= len(cadea) ) = devolve a posición na que se atopou por primeira vez a subcadea dende comezo ata final
.join( listadecadeas ) = introduce a cadea entre cada par de cadeas da lista
.partition( sep ) = devolve unha tupla con tres cadeas: unha coa cadea inicial ata sep, outra con sep e a última cunha cadea dende sep ata o final. Se non atopa sep devolve as dúas últimas baleiras
.replace( subcadea, substituto, nveces=1 ) devolve unha cadea onde reempraza nveces a subcadea polo substituto
.split( sep=' ', nmax= inf ) devolve unha lista coas subcadeas que forman a inicial separadas por sep un máximo de nmax veces.

#Opcions de texto:
\n = salto de liña
\t = espazo horizontal

#Operadores booleanos:
Calquera cousa distinta de 0 é interpretado como un 1 a nivel lóxico.
0 = False
1 = True
a and b = True se e só se a=b=True, False en caso contrario
a or b = False só se a=b=False
not b = True se b = False e viceversa

a == b: True se a = b, False en caso contrario
a != b: False se a = b, True en caso contrario
a < b: True se a < b.
a > b: True se a > b.
a <= b: True se a < b ou a = b.

#Listas:
listas: a = [ 1, 2, 3, [1, 2, 3], 'a', 'b', 'c', 0.9, 1+3j, True ]
a[0] = 1 #as listas comezan en 0 e rematan en n-1
a[3] = [1, 2, 3] #un dos elementos pode ser outra lista
a[3][2] = 3 #para acceder aos elementos dunha sublista basta con poñer outro índice
a[-1]= True # os número negativos toman os elementos comezando polo último, sen 0
a[4:7] = ['a', 'b', 'c'] #x:y toma os elementos de x ata y-1
a[4:9:2] = [ 'a', 'c', 1+3j ] #x:y:z toma os elementos de x ata y-1 en saltos de z
a[:3] = [1, 2, 3] # :x colle os elementos ata o x-1
a[0:3] = [1,2,3,4,5,6,7,8,9] -> a = [ [1,2,3,4,5,6,7,8,9], [1,2,3], ...]

Métodos:
.append( valor ) engade valor ao final
.count( valor ) conta o número de veces que aparece valor na lista
.extend( iterable ) engade os elementos do iterable na lista
.index( valor, comezo=0, final= len(lista) ) devolve o número de veces que se atopou valor na lista dende comezo ata final
.insert( índice, valor ) inserta valor na posición índice
.pop( indice=len(lista) ) devolve o valor na posición índice e elimina o elemento
.remove( valor ) elimina o 1º elemento que coincida con valor
del nomelista[x] elimina o elemento x
.reverse() invirte a lista (non se pode asignar a outra variable)
.sort( cmp = None, key=None, reverse=False ) ordea a lista

#Listas inline:
[ operación ordes ] crea unha nova lista a partir das ordes. p. ex:
    [ n**2 for n in l if n>0] collería cada elemento de l e elevaríao ao cadrado se é positivo resultando nunha nova lista

#Xeradores
( operación ordes ) crea un xerador de listas. Define a operación para crear a lista, pero non a constrúe, se non que ofrece funcións para acceder aos sucesivos elementos. p. ex.: g = (n**2 for n in l) con l=[0,1,2,3]

#Dicionarios:
a = { chave1 : valor1, chave2 : valor2, ...}
a[chave1] = valor1

Métodos:
.keys() = accede á lista de chaves
.valuers() = accede á lista de valores
.items() = accede á lista de pares chave-valor
.get(a,b) = se existe a como chave devolve nomedic[a], se non, b
.has_key(k) = True se existe a chave k, se non, False
.pop(a,b) = borra a clave a e devolve o seu valor. Se non existe devolve b.


para acceder á lista de chaves: nomedic.keys()
para acceder á lista de valores: nomedic.values()
para acceder á lista de pares chave-valor: nomedis.items()

#Condicionais:
if condición1:
    cousas #ten que ir indentado
elif condición2:
    máis cousas #ten que ir indentado
else:
    outras cousas distintas #ten que ir indentado

versión curta: D =A if B else C. Avalía B, se é True D = A, se non, D = C
podense unir condicións cos operadores booleanos: if a and not (b or c): blablabla

#Bucles:
while (condición):
    cousas #mentres se cumpra a condición repetirá o bucle. Ten que ir indentado

for var in lista:
    cousas #var toma os valores de lista de un en un e procesa cousas

range(x) crea unha lista que vai de 0 a x-1 de un en un
range(y,x) crea unha lista que vai de y a x-1 de un en un
range(y,x,z) crea unha lista que vai de y a x-1 de z en z

#Funcións:
def nomefunción( parámetro1, parámetro2, ..., parámetron):
    '''Documentación'''
    ordes

para que a función devolva valores:
return variable1, variable2, ...

poñer na definición parámetrok = tanto fai que ese parámetro teña ese valor por defecto. Se ao chamar á función non incluimos ese parámetro tomará o valor por defecto. De incluilo tomará o valor pasado.

se se pon ao final un parámetro cun asterisco antes, o número de argumentos é aumentable. O número de argumentos extra é tratado coma unha tupla. p. ex:
def funcion(a,b,*c):
    print a,b
    for i in c:
        print i
funcion(1,2,3,4,5) daría como resultado:
1 2
3
4
5

se se fai o mesmo con dous asteriscos os argumentos extra serán parte dun diccionario. Os argumentos extra débense dispoñer do xeito clave = valor. p. ex:
def funcion(a,b,**c):
    print a,b
    for i in c: #Equivalente a for i in c.keys():
        print i,c[i]
funcion(1,2,a=3,b=4,c=5) daría como resultado:
1 2
a 3
b 4
c 5

#Funcións especiais:
map( función, lista1, lista2, ...): pasa cada elemento das listas como parámetros á función. Cando se meten n listas é porque a función acepta n argumentos.

filter( función, lista ): pasa os elementos de lista pola función. Devolve unha lista con aqueles que dan True ao ser pasados á función.p. ex. cunha función que che diga se un número é par, filter( epar, [0,1,2,3,4] ) daría [0,2,4].

reduce( función, lista, inicial=0 ): aplica a función iterativamente sobre pares de elementos da lista ata deixala cun só valor. Engade este resultado a inicial. p. ex. cunha función sumar(x,y) e l=[0,1,2,3], reduce(sumar,l) faría:
    suma 3 e 2 -> [0,1,5]
    suma 1 e 5 -> [0,6]
    suma 0 e 6 -> [6]
    devolve 6

lambda p1,p2,...,pn: definiciondafuncion: lambda declara no momento unha función anónima de parámetros p1,...,pn. Serve para funcións que só se usan unha vez, polo que non lle fai falta nome para chamala. Útiles á hora de pasar funcións como parámetro.

#Decoradores
def decorador( función ):
    ordes
    return outrafunción

serve para engadir funcionalidades ás funcións, por exemplo engadir un print que diga que a estás chamando. Para aplicar decoradores engadir antes da definicion da función: p.ex.:

@nomedodecorador3 #os decoradores lense de abaixo cara arriba
@nomedodecorador2
@nomedodecorador1
def función():
    ...


#Clases:
class nomedaclase:
    '''Documentación'''
    def __init__(self, parámetros): #Inicializador de obxetos
        cousas
    datos membro ...
    métodos ...

o primeiro argumento dun método dunha clase é sempre self, para indicar que se pode acceder aos elementos da clase e diferenciar de paso variables locais das da clase. por exemplo poderíamos ter definida unha variable var no código xeral e tamén na clase. Para acceder a esta última: self.var

Crear un obxecto dunha certa clase:
nomeobxecto = nomedaclase(parámetros de __init__ )
onde nos parámetros nunca se inclúe self.

para crear unha clase que herede de outra:
class nomedasubclase( nomedasuperclase1, nomedasuperclase2, ... ):
    ...

Pódese chamar aos métodos da súperclase do xeito habitual:
nomedasuperclase.metodo(self, argumentos ). Neste caso é obligatorio usar self.

atributos e métodos privados: comezan con __ e non rematan con __. p. ex:
def __privado(self):
    print 'Aquí non se entra máis que dende a propia clase'

pódese facer unha pequena trampa para acceder igualmente aos métodos privados:

nomeobxecto._nomeclase__nomemetodo()

no caso de usar setters e getters pódese usar o seguinte:
__var é un atributo privado.
getvar(self) devolve o valor de __var
setvar(self) asigna un valor a __var
como é privado nunha poderíamos facer un nomeobxecto.__var nin nomeobxecto.var =...

pero se poñemos... var = property( getvar, setvar ) podemos facer nomeobxecto.var = ...
para poder usar isto a clase debe derivar de object: nomedaclase(object): ...

#Métodos especiais:
__init__( self, argumentos ) inicializa
__new__( nomedaclase, argumentos ) constructor
__del__( self ) destructor
__str__( self ) devolve unha cadena de texto que representa ao obxecto
__cmp__( self, IDdeoutroobxecto ) compara obxectos
__len__( self ) lonxitude do obxecto

#Excepcións
Trata unha orde e, en caso de que haxa un problema pódese realizar unha execución alternativa.
try:
    fai isto
except:
    houbo un erro, entón fai isto outro
else:
    non houbo erro
finally:
    isto faise sempre

#Módulos
podemos ter un ficheiro que conteña funcións, datos, etc. e podemos importalo para usalos noutro código. Se temos un modulo.py no mesmo directorio que o noso programa, ao principio deste poñemos:

import modulo1, modulo2, modulo3
modulo1.función(parámetros) para usar unha función definida en modulo1
modulo3.variable para usar unha variable definida en modulo3

Ao importar execútase o código do módulo, de xeito que se fará todo o que conteña o script.

Para non ter que indicar o nome do módulo antes de usar unha función ou variable:
from modulo1 import función, variable
from modulo import * importa todo de modulo
para importar módulos de outros directorios debemos incorporar estes módulos ao PYTHONPATH:
import sys
sys.path.append('ruta do directorio')

#Ficheiros

nomeficheiro = open( 'nomearquivo.extensión', 'modoapertura' ) abre un ficheiro
nomeficheiro.close() pecha o ficheiro aberto

Modos de apertura:
'w' sobreescribir
'r' ler
'a' engadir ao final
'b' binario
'+' ler e escribir
'U' saltos de liña universal

Formas de ler:
.read( n=todo ) le n bytes. Se se omite le todo.
.readlines() le tódalas liñas do ficheiro e gárdaas nunha lista
.readline() le unha liña. Cada vez que se usa o punteiro de lectura avanza unha liña.

Formas de escribir:
.write( cadea ) escribe cadea no arquivo. Para números úsese str(número). Hai que poñer os saltos de liña explícitamente como '\n'
.writelines( lista ) escribe cada elemento da lista. Non sei se pon saltos de liña.

Punteiro de lectura/escritura:
tell() devolve a distancia en bytes dende o principio do ficheiro ata onde se atopa o punteiro
seek( n, pos=0 ) move o punteiro n bytes dende pos.
pos=0: dende o principio
pos=1: dende onde está agora
pos=2: dende o final

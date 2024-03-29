import json
from flask import Flask, render_template, request, redirect, url_for, escape

app = Flask(__name__)

max_results = 20

bloom_verbs_lists = [
    #remember
    ["remember", "cite","define","describe","draw","enumerate","identify","index","indicate","label","list","match","meet","name","outline","point","quote","read","recall","recite","recognize","record","repeat","reproduce","review","select","state","study","tabulate","trace","write","interpret","observe","paraphrase","picture graphically","predict","review","rewrite","subtract","summarize","translate","visualize","personalize","plot","practice","predict","prepare","price","process","produce","project","provide","relate","round off","sequence","show","simulate","sketch","solve","subscribe","tabulate","transcribe","translate","use","recordar", "citar","definar","describir","dibujar","enumerar","identificar","memorizar","indicar","etiquetar","listar","asignar","caracterizar","nombrar","recitar","resumir","citar","leer","recordra","memorizar","reconocer","acordar","repetir","reproducir","revisar","seleccionar","afirmar","estudiar","tabular","trazar","escribir","interpretar","observar","parafrasear","encontrar","predecir","revisar","reescribir","restar","resumir","traducir","visualizar","personalizar","dibujar","graficar","predecir","preparar","justificar","procesar","producir","proyectar","proporcionra","relatar","narrar","secuenciar","mostrar","simular","bosquejar","resolver","suscribir","tabular","transcribir","traducir","usar"],
    #understand
    ["understand","add","approximate","articulate","associate","characterize","clarify","classify","compare","compute","contrast","convert","defend","describe","detail","differentiate","discuss","distinguish","elaborate","estimate","example","explain","express","extend","extrapolate","factor","generalize","give","infer","interact","interpolate","express","factor","figure","graph","handle","illustrate","interconvert","investigate","manipulate","modify","operate","proofread","query","relate","select","separate","subdivide","train","transform","entender","añadir","aproximar","articular","asociar","caracterizar","aclarar","clasificar","comparar","computar","contrastar","convertir","defender","describir","detallar","diferenciar","discutir","identificar","elaborar","estimar","ejemplificar","explicar","expresar","extender","extrapolar","reescribir","generalizar","dar","inferir","interactuar","interpolar","expresar","factorizar","figurar","graficar","manipular","ilustrar","convertir","investigar","manipular","modificar","operar","revisar","consultar","relacionar","seleccionar","separar","subdividir","entrenar","transformar"],
    #analyze
    ["analyze"," analyze","audit","blueprint","breadboard","break down","characterize","classify","compare","confirm","contrast","correlate","detect","diagnose","diagram","differentiate","discriminate","dissect","distinguish","document","ensure","examine","explain","explore","figure out","file","group","identify","illustrate","infer","interrupt","validate","verify","overhaul","plan","portray","prepare","prescribe","produce","program","rearrange","reconstruct","relate","reorganize","revise","rewrite","specify","summarize","analizar","auditar","ponderar","considerar","particularizar","caracterizar","clasificar","comparar","confirmar","contrastar","correlar","detectar","diagnosticar","dibujar","diferenciar","discriminar","diseccionar","distinguir","documentar","asegurar","examinar","explicar","explorar","archivar","implementar","agrupar","identificar","ilustrar","inferir","interrumpir","validar","verificar"],
    #apply
    ["apply","acquire","adapt","allocate","alphabetize","apply","ascertain","assign","attain","avoid","back up","calculate","capture","change","classify","complete","compute","construct","customize","demonstrate","depreciate","derive","determine","diminish","discover","draw","employ","examine","exercise","explore","expose","inventory","investigate","layout","manage","maximize","minimize","optimize","order","outline","point out","prioritize","aplicar","adquirir","adaptar","ubicar","alfabetizar","determinar","asignar","obtener","evitar","respaldar","calcular","capturar","desarrollar","cambiar","clasificar","completar","computar","programar","demostrar","implementar","derivar","determinar","reducir","simplificar","descubrir","dibujar","emplear","examinar","explorar","exponer","inventar","investigar","trazar","gestionar","maximizar","optimizar","minimizar","ordenar","compilar","calibrar","priorizar"],
    #evaluate
    ["evaluate","appraise","assess","compare","conclude","contrast","counsel","criticize","critique","defend","determine","discriminate","estimate","evaluate","explain","grade","hire","interpret","judge","justify","measure","predict","prescribe","rank","rate","recommend","release","select","summarize","support","test","improve","incorporate","integrate","interface","join","lecture","model","modify","network","organize","outline","evaluar","valorar","assess","comparar","concluir","contrastar","aconsejar","criticar","critique","defender","determinar","discriminar","estimular","evaluar","explicar","puntuar","contratar","interpretar","juzgar","justificar","medir","predecir","anticipar","prescribir","ordenar","recomendar","lanzar","seleccionar","resumir","apoyar","testear","mejorar","incorporar","integrar","combinar","presentar","modelar","modificar","conectar","organizar"],
    #create
    ["create","abstract","animate","arrange","assemble","budget","categorize","code","combine","compile","compose","construct","cope","correspond","create","cultivate","debug","depict","design","develop","devise","dictate","enhance","explain","facilitate","format","formulate","generalize","generate","handle","import","crear","abstraer","animar","diseñar","ensamblar","presupuestar","categorizar","codificar","combinar","compilar","componer","construir","resolver","corresponder","crear","cultivar","depurar","mostrar","diseñar","desarollar","concebir","dictar","mejorar","explicar"]
]

# Returns occurrences of a verb in a text
def count_verbs(course_description,verbs_list):
    return sum(course_description.lower().count(verb.lower()) for verb in verbs_list)

#Checks the bloom verbs
def count_bloom_verbs(course_description):
    total_verbs = 0
    bloom_count = []
    res = []
    for verb_list in bloom_verbs_lists:
        count = count_verbs(course_description,verb_list)
        total_verbs += count
        bloom_count.append(count)
    for num in bloom_count:
        try:
            res.append('{:.1f}'.format(num/total_verbs*100))
        except:
            # If there's no description, no verbs can be counted
            return [0,0,0,0,0,0]
    return res

def get_course(query,max):
    res = []
    with open('spiders/course_crawler_data/all.json','r') as f:
        data = json.load(f)

    i=1
    try:
        for course in data:
            if i==max:
                break
            if query.lower() in course['name'].lower() or query.lower() in course['skills'] or query.lower() in course['description'] or query.lower() in course['outcomes']:
                res.append(course)       
                i+=1
    except:
        print('----------------------------')
    
    print(f'Courses shown: {len(res)}')
    return res

@app.route('/', methods=['GET','POST'])
def index():
    return render_template('index.html')


@app.route('/search', methods=['GET','POST'])
def search():
    search_query = request.form['search']
    print("Search query:", search_query)

    courses = get_course(search_query,max_results)
    if courses == []:
        return render_template('no_results.html')

    bloom_arr = []
    for course in courses:
        bloom_count = count_bloom_verbs(course['description'])
        bloom_arr.append(bloom_count)

    return render_template('results.html', courses=courses, bloom_nums=bloom_arr, limit=min(max_results, len(courses)))


if __name__ == '__main__':
    app.run(debug=True)

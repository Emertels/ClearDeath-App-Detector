import winreg
import os
import re
import sys
import ctypes
import subprocess
from datetime import datetime


# ============================================================
# CONFIGURAÇÃO
# ============================================================

REGISTRY_PATHS = [
    (
        winreg.HKEY_LOCAL_MACHINE,
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
        "HKLM 64-bit"
    ),
    (
        winreg.HKEY_LOCAL_MACHINE,
        r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall",
        "HKLM 32-bit"
    ),
    (
        winreg.HKEY_CURRENT_USER,
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
        "HKCU"
    ),
]


# Programas que são desinstaladores do próprio Windows.
# Nunca vamos considerar esses caminhos como "mortos".
WINDOWS_INSTALLERS = {
    "msiexec.exe",
    "msiexec",
}


# ============================================================
# CORES DO TERMINAL
# ============================================================

class C:
    RESET = "\033[0m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    GRAY = "\033[90m"
    BOLD = ""
SESSION_LABELS = {
    "pt-BR": ("Versão", "Sessão iniciada em", "Idioma detectado"),
    "en": ("Version", "Session started", "Detected language"),
    "es": ("Versión", "Sesión iniciada", "Idioma detectado"),
    "fr": ("Version", "Session démarrée", "Langue détectée"),
    "de": ("Version", "Sitzung gestartet", "Erkannte Sprache"),
    "it": ("Versione", "Sessione avviata", "Lingua rilevata"),
    "ja": ("バージョン", "セッション開始", "検出された言語"),
    "ko": ("버전", "세션 시작", "감지된 언어"),
    "zh-CN": ("版本", "会话开始时间", "检测到的语言"),
    "ru": ("Версия", "Сеанс начат", "Обнаруженный язык"),
}

MENU_TEXT = {
    "pt-BR": ("MENU", "Mostrar novamente os inativos", "Ver suspeitos", "Selecionar entradas para remover", "Remover TODOS os encontrados", "Sair", "Escolha: "),
    "en": ("MENU", "Show inactive entries again", "View suspicious entries", "Select entries to remove", "Remove ALL found entries", "Exit", "Choose: "),
    "es": ("MENÚ", "Mostrar de nuevo los inactivos", "Ver sospechosos", "Seleccionar entradas para eliminar", "Eliminar TODAS las entradas encontradas", "Salir", "Elija: "),
    "fr": ("MENU", "Afficher de nouveau les entrées inactives", "Voir les éléments suspects", "Sélectionner les entrées à supprimer", "Supprimer TOUTES les entrées trouvées", "Quitter", "Choix : "),
    "de": ("MENÜ", "Inaktive Einträge erneut anzeigen", "Verdächtige Einträge anzeigen", "Einträge zum Entfernen auswählen", "ALLE gefundenen Einträge entfernen", "Beenden", "Auswahl: "),
    "it": ("MENU", "Mostra di nuovo le voci inattive", "Visualizza le voci sospette", "Seleziona le voci da rimuovere", "Rimuovi TUTTE le voci trovate", "Esci", "Scelta: "),
    "ja": ("メニュー", "非アクティブな項目を再表示", "疑わしい項目を表示", "削除する項目を選択", "見つかった項目をすべて削除", "終了", "選択: "),
    "ko": ("메뉴", "비활성 항목 다시 표시", "의심 항목 보기", "삭제할 항목 선택", "찾은 항목 모두 삭제", "종료", "선택: "),
    "zh-CN": ("菜单", "再次显示无效条目", "查看可疑条目", "选择要删除的条目", "删除所有找到的条目", "退出", "选择："),
    "ru": ("МЕНЮ", "Показать неактивные записи снова", "Показать подозрительные записи", "Выбрать записи для удаления", "Удалить ВСЕ найденные записи", "Выход", "Выберите: "),
}


RESULT_LABELS = {
    "pt-BR": ("RESULTADO DA ANÁLISE", "Total analisado", "MORTOS", "SUSPEITOS", "ENTRADAS PROVAVELMENTE MORTAS", "Nenhuma entrada foi confirmada como morta.", "OK", "MORTO", "SUSPEITO"),
    "en": ("ANALYSIS RESULTS", "Total analyzed", "DEAD", "SUSPICIOUS", "PROBABLY DEAD ENTRIES", "No entries were confirmed as dead.", "OK", "DEAD", "SUSPICIOUS"),
    "es": ("RESULTADOS DEL ANÁLISIS", "Total analizado", "MUERTOS", "SOSPECHOSOS", "ENTRADAS PROBABLEMENTE MUERTAS", "Ninguna entrada fue confirmada como muerta.", "OK", "MUERTO", "SOSPECHOSO"),
    "fr": ("RÉSULTATS DE L’ANALYSE", "Total analysé", "INACTIFS", "SUSPECTS", "ENTRÉES PROBABLEMENT INACTIVES", "Aucune entrée n’a été confirmée comme inactive.", "OK", "INACTIF", "SUSPECT"),
    "de": ("ANALYSEERGEBNISSE", "Insgesamt geprüft", "INAKTIV", "VERDÄCHTIG", "WAHRSCHEINLICH INAKTIVE EINTRÄGE", "Es wurde kein Eintrag als inaktiv bestätigt.", "OK", "INAKTIV", "VERDÄCHTIG"),
    "it": ("RISULTATI DELL’ANALISI", "Totale analizzato", "INATTIVI", "SOSPETTI", "VOCI PROBABILMENTE INATTIVE", "Nessuna voce è stata confermata come inattiva.", "OK", "INATTIVO", "SOSPETTO"),
    "ja": ("分析結果", "分析した合計", "無効", "疑わしい項目", "無効の可能性がある項目", "無効と確認された項目はありません。", "OK", "無効", "疑わしい"),
    "ko": ("분석 결과", "분석된 항목", "비활성", "의심 항목", "비활성일 가능성이 있는 항목", "비활성으로 확인된 항목이 없습니다.", "정상", "비활성", "의심"),
    "zh-CN": ("分析结果", "分析总数", "无效", "可疑", "可能无效的条目", "没有条目被确认无效。", "正常", "无效", "可疑"),
    "ru": ("РЕЗУЛЬТАТЫ АНАЛИЗА", "Проверено всего", "НЕАКТИВНЫЕ", "ПОДОЗРИТЕЛЬНЫЕ", "ВЕРОЯТНО НЕАКТИВНЫЕ ЗАПИСИ", "Не удалось подтвердить ни одной неактивной записи.", "OK", "НЕАКТИВНО", "ПОДОЗРИТЕЛЬНО"),
}


ANALYSIS_REASONS = {
    "pt-BR": ("Pasta de instalação encontrada.", "Executável associado ao aplicativo encontrado.", "Desinstalador encontrado.", "Usa Windows Installer (MSI).", "Pasta de instalação e referências principais não foram encontradas.", "Não foi possível confirmar se o aplicativo está instalado."),
    "en": ("Installation folder found.", "Application executable found.", "Uninstaller found.", "Uses Windows Installer (MSI).", "The installation folder and primary references were not found.", "Could not confirm whether the application is installed."),
    "es": ("Se encontró la carpeta de instalación.", "Se encontró el ejecutable asociado a la aplicación.", "Se encontró el desinstalador.", "Usa Windows Installer (MSI).", "No se encontraron la carpeta de instalación ni las referencias principales.", "No se pudo confirmar si la aplicación está instalada."),
    "fr": ("Dossier d’installation trouvé.", "Exécutable associé à l’application trouvé.", "Programme de désinstallation trouvé.", "Utilise Windows Installer (MSI).", "Le dossier d’installation et les références principales sont introuvables.", "Impossible de confirmer si l’application est installée."),
    "de": ("Installationsordner gefunden.", "Zugehörige Anwendungsdatei gefunden.", "Deinstallationsprogramm gefunden.", "Verwendet Windows Installer (MSI).", "Installationsordner und wichtige Verweise wurden nicht gefunden.", "Der Installationsstatus der Anwendung konnte nicht bestätigt werden."),
    "it": ("Cartella di installazione trovata.", "Eseguibile associato all’applicazione trovato.", "Programma di disinstallazione trovato.", "Usa Windows Installer (MSI).", "Cartella di installazione e riferimenti principali non trovati.", "Impossibile confermare se l’applicazione è installata."),
    "ja": ("インストールフォルダーが見つかりました。", "アプリに関連付けられた実行ファイルが見つかりました。", "アンインストーラーが見つかりました。", "Windows Installer (MSI) を使用しています。", "インストールフォルダーと主な参照先が見つかりません。", "アプリがインストールされているか確認できませんでした。"),
    "ko": ("설치 폴더를 찾았습니다.", "앱과 연결된 실행 파일을 찾았습니다.", "제거 프로그램을 찾았습니다.", "Windows Installer(MSI)를 사용합니다.", "설치 폴더와 주요 참조 항목을 찾을 수 없습니다.", "앱의 설치 여부를 확인할 수 없습니다."),
    "zh-CN": ("已找到安装文件夹。", "已找到与应用关联的可执行文件。", "已找到卸载程序。", "使用 Windows Installer (MSI)。", "未找到安装文件夹和主要引用项。", "无法确认应用是否已安装。"),
    "ru": ("Папка установки найдена.", "Исполняемый файл приложения найден.", "Программа удаления найдена.", "Используется Windows Installer (MSI).", "Папка установки и основные ссылки не найдены.", "Не удалось подтвердить, установлено ли приложение."),
}


ACTION_TEXT = {'pt-BR': ('Este programa precisa de administrador.',
           'Solicitando permissão do Windows...',
           'Não foi possível obter permissão.',
           'Erro ao solicitar administrador: {error}',
           'Analisando o Registro do Windows...',
           'Isso pode levar alguns segundos.',
           'Nenhuma entrada selecionada.',
           'VOCÊ ESTÁ PRESTES A REMOVER ENTRADAS DO REGISTRO',
           'Isso NÃO desinstala os arquivos dos programas.',
           'Isso apenas remove a entrada da lista de aplicativos do Windows.',
           'Digite "REMOVER" para continuar: ',
           'Operação cancelada.',
           'A remoção foi cancelada porque o backup do Registro não foi concluído.',
           'Pressione ENTER para continuar...',
           'Removendo entradas...',
           'Removendo: {name}',
           '✓ Removido',
           '{success}/{total} entradas removidas.',
           'SELEÇÃO',
           'Digite os números que deseja remover.',
           'Exemplo: 1,3,5',
           'Digite ALL para selecionar todos.',
           'Digite 0 para cancelar.',
           'Seleção: ',
           'Backup criado em:\n{path}',
           'Backup incompleto: {error}. Nenhuma entrada será removida.',
           '⚠ AVISO: A pasta de instalação ainda existe!',
           'Removendo somente a entrada do Registro...',
           'Permissão negada.',
           'Erro: {error}'),
 'en': ('This program requires administrator privileges.',
        'Requesting Windows permission...',
        'Could not obtain administrator permission.',
        'Error requesting administrator access: {error}',
        'Scanning the Windows Registry...',
        'This may take a few seconds.',
        'No entries selected.',
        'YOU ARE ABOUT TO REMOVE REGISTRY ENTRIES',
        'This does NOT uninstall the program files.',
        'This only removes the entry from the Windows apps list.',
        'Type "REMOVER" to continue: ',
        'Operation cancelled.',
        'Removal cancelled because the Registry backup did not complete.',
        'Press Enter to continue...',
        'Removing entries...',
        'Removing: {name}',
        '✓ Removed',
        '{success}/{total} entries removed.',
        'SELECTION',
        'Enter the numbers to remove.',
        'Example: 1,3,5',
        'Type ALL to select every entry.',
        'Type 0 to cancel.',
        'Selection: ',
        'Backup created at:\n{path}',
        'Backup incomplete: {error}. No entries will be removed.',
        '⚠ WARNING: The installation folder still exists!',
        'Removing only the Registry entry...',
        'Permission denied.',
        'Error: {error}'),
 'es': ('Este programa requiere permisos de administrador.',
        'Solicitando permiso de Windows...',
        'No se pudieron obtener permisos de administrador.',
        'Error al solicitar permisos de administrador: {error}',
        'Analizando el Registro de Windows...',
        'Esto puede tardar unos segundos.',
        'No se seleccionaron entradas.',
        'ESTÁ A PUNTO DE ELIMINAR ENTRADAS DEL REGISTRO',
        'Esto NO desinstala los archivos de los programas.',
        'Esto solo elimina la entrada de la lista de aplicaciones de Windows.',
        'Escriba "REMOVER" para continuar: ',
        'Operación cancelada.',
        'Eliminación cancelada porque no se completó la copia de seguridad del Registro.',
        'Presione ENTER para continuar...',
        'Eliminando entradas...',
        'Eliminando: {name}',
        '✓ Eliminado',
        '{success}/{total} entradas eliminadas.',
        'SELECCIÓN',
        'Escriba los números que desea eliminar.',
        'Ejemplo: 1,3,5',
        'Escriba ALL para seleccionar todas.',
        'Escriba 0 para cancelar.',
        'Selección: ',
        'Copia de seguridad creada en:\n{path}',
        'Copia incompleta: {error}. No se eliminará ninguna entrada.',
        '⚠ AVISO: ¡La carpeta de instalación todavía existe!',
        'Se eliminará solo la entrada del Registro...',
        'Permiso denegado.',
        'Error: {error}'),
 'fr': ('Ce programme nécessite les droits d’administrateur.',
        'Demande d’autorisation Windows...',
        'Impossible d’obtenir les droits d’administrateur.',
        'Erreur lors de la demande des droits administrateur : {error}',
        'Analyse du Registre Windows...',
        'Cela peut prendre quelques secondes.',
        'Aucune entrée sélectionnée.',
        'VOUS ALLEZ SUPPRIMER DES ENTRÉES DU REGISTRE',
        'Cela NE désinstalle PAS les fichiers des programmes.',
        'Cela supprime uniquement l’entrée de la liste des applications Windows.',
        'Saisissez "REMOVER" pour continuer : ',
        'Opération annulée.',
        'Suppression annulée : la sauvegarde du Registre n’est pas terminée.',
        'Appuyez sur Entrée pour continuer...',
        'Suppression des entrées...',
        'Suppression : {name}',
        '✓ Supprimé',
        '{success}/{total} entrées supprimées.',
        'SÉLECTION',
        'Saisissez les numéros à supprimer.',
        'Exemple : 1,3,5',
        'Saisissez ALL pour tout sélectionner.',
        'Saisissez 0 pour annuler.',
        'Sélection : ',
        'Sauvegarde créée dans :\n{path}',
        'Sauvegarde incomplète : {error}. Aucune entrée ne sera supprimée.',
        '⚠ ATTENTION : le dossier d’installation existe toujours !',
        'Suppression de la seule entrée du Registre...',
        'Accès refusé.',
        'Erreur : {error}'),
 'de': ('Dieses Programm benötigt Administratorrechte.',
        'Windows-Berechtigung wird angefordert...',
        'Administratorrechte konnten nicht angefordert werden.',
        'Fehler beim Anfordern der Administratorrechte: {error}',
        'Windows-Registrierung wird analysiert...',
        'Dies kann einige Sekunden dauern.',
        'Keine Einträge ausgewählt.',
        'SIE SIND DABEI, REGISTRIERUNGSEINTRÄGE ZU ENTFERNEN',
        'Dies deinstalliert NICHT die Programmdateien.',
        'Dies entfernt nur den Eintrag aus der Windows-App-Liste.',
        'Geben Sie "REMOVER" ein, um fortzufahren: ',
        'Vorgang abgebrochen.',
        'Entfernung abgebrochen, da die Registrierungssicherung nicht abgeschlossen wurde.',
        'Drücken Sie Enter, um fortzufahren...',
        'Einträge werden entfernt...',
        'Entferne: {name}',
        '✓ Entfernt',
        '{success}/{total} Einträge entfernt.',
        'AUSWAHL',
        'Geben Sie die Nummern der zu entfernenden Einträge ein.',
        'Beispiel: 1,3,5',
        'Geben Sie ALL ein, um alle auszuwählen.',
        'Geben Sie 0 zum Abbrechen ein.',
        'Auswahl: ',
        'Sicherung erstellt unter:\n{path}',
        'Sicherung unvollständig: {error}. Es werden keine Einträge entfernt.',
        '⚠ WARNUNG: Der Installationsordner ist noch vorhanden!',
        'Es wird nur der Registrierungseintrag entfernt...',
        'Zugriff verweigert.',
        'Fehler: {error}'),
 'it': ('Questo programma richiede i privilegi di amministratore.',
        'Richiesta di autorizzazione di Windows...',
        'Impossibile ottenere i privilegi di amministratore.',
        'Errore durante la richiesta dei privilegi di amministratore: {error}',
        'Analisi del Registro di Windows...',
        'L’operazione potrebbe richiedere alcuni secondi.',
        'Nessuna voce selezionata.',
        'STAI PER RIMUOVERE VOCI DAL REGISTRO',
        'Questa operazione NON disinstalla i file dei programmi.',
        'Rimuove solo la voce dall’elenco delle app di Windows.',
        'Digita "REMOVER" per continuare: ',
        'Operazione annullata.',
        'Rimozione annullata: il backup del Registro non è stato completato.',
        'Premi INVIO per continuare...',
        'Rimozione delle voci...',
        'Rimozione: {name}',
        '✓ Rimosso',
        '{success}/{total} voci rimosse.',
        'SELEZIONE',
        'Digita i numeri delle voci da rimuovere.',
        'Esempio: 1,3,5',
        'Digita ALL per selezionare tutte le voci.',
        'Digita 0 per annullare.',
        'Selezione: ',
        'Backup creato in:\n{path}',
        'Backup incompleto: {error}. Nessuna voce verrà rimossa.',
        '⚠ ATTENZIONE: la cartella di installazione esiste ancora!',
        'Verrà rimossa solo la voce del Registro...',
        'Accesso negato.',
        'Errore: {error}'),
 'ja': ('このプログラムには管理者権限が必要です。',
        'Windows の許可を要求しています...',
        '管理者権限を取得できませんでした。',
        '管理者権限の要求中にエラーが発生しました: {error}',
        'Windows レジストリを分析しています...',
        '数秒かかる場合があります。',
        '項目が選択されていません。',
        'レジストリ項目を削除しようとしています',
        'プログラムファイルはアンインストールされません。',
        'Windows アプリ一覧の項目だけを削除します。',
        '続行するには "REMOVER" と入力してください: ',
        '操作をキャンセルしました。',
        'レジストリのバックアップが完了しなかったため、削除を中止しました。',
        '続行するには Enter キーを押してください...',
        '項目を削除しています...',
        '削除中: {name}',
        '✓ 削除済み',
        '{success}/{total} 件の項目を削除しました。',
        '選択',
        '削除する項目の番号を入力してください。',
        '例: 1,3,5',
        'すべて選択するには ALL と入力してください。',
        'キャンセルするには 0 と入力してください。',
        '選択: ',
        'バックアップを保存しました:\n{path}',
        'バックアップが不完全です: {error}。項目は削除されません。',
        '⚠ 注意: インストールフォルダーがまだ存在します。',
        'レジストリ項目のみを削除します...',
        'アクセスが拒否されました。',
        'エラー: {error}'),
 'ko': ('이 프로그램에는 관리자 권한이 필요합니다.',
        'Windows 권한을 요청하는 중...',
        '관리자 권한을 얻지 못했습니다.',
        '관리자 권한 요청 오류: {error}',
        'Windows 레지스트리를 분석하는 중...',
        '몇 초 정도 걸릴 수 있습니다.',
        '선택된 항목이 없습니다.',
        '레지스트리 항목을 제거하려고 합니다',
        '프로그램 파일은 제거되지 않습니다.',
        'Windows 앱 목록에서 항목만 제거합니다.',
        '계속하려면 "REMOVER"를 입력하세요: ',
        '작업이 취소되었습니다.',
        '레지스트리 백업이 완료되지 않아 제거를 취소했습니다.',
        '계속하려면 Enter 키를 누르세요...',
        '항목을 제거하는 중...',
        '제거 중: {name}',
        '✓ 제거됨',
        '{total}개 중 {success}개 항목을 제거했습니다.',
        '선택',
        '제거할 항목 번호를 입력하세요.',
        '예: 1,3,5',
        '모두 선택하려면 ALL을 입력하세요.',
        '취소하려면 0을 입력하세요.',
        '선택: ',
        '백업 저장 위치:\n{path}',
        '백업이 불완전합니다: {error}. 항목을 제거하지 않습니다.',
        '⚠ 경고: 설치 폴더가 아직 있습니다.',
        '레지스트리 항목만 제거합니다...',
        '액세스가 거부되었습니다.',
        '오류: {error}'),
 'zh-CN': ('此程序需要管理员权限。',
           '正在请求 Windows 权限...',
           '无法获取管理员权限。',
           '请求管理员权限时出错：{error}',
           '正在分析 Windows 注册表...',
           '这可能需要几秒钟。',
           '未选择任何条目。',
           '即将删除注册表条目',
           '此操作不会卸载程序文件。',
           '此操作只会从 Windows 应用列表中删除条目。',
           '输入 "REMOVER" 以继续：',
           '操作已取消。',
           '注册表备份未完成，已取消删除。',
           '按 Enter 键继续...',
           '正在删除条目...',
           '正在删除：{name}',
           '✓ 已删除',
           '已删除 {success}/{total} 个条目。',
           '选择',
           '输入要删除的条目编号。',
           '例如：1,3,5',
           '输入 ALL 以选择全部条目。',
           '输入 0 以取消。',
           '选择：',
           '备份已创建：\n{path}',
           '备份不完整：{error}。不会删除任何条目。',
           '⚠ 注意：安装文件夹仍然存在！',
           '仅删除注册表条目...',
           '访问被拒绝。',
           '错误：{error}'),
 'ru': ('Для этой программы нужны права администратора.',
        'Запрос разрешения Windows...',
        'Не удалось получить права администратора.',
        'Ошибка запроса прав администратора: {error}',
        'Анализ реестра Windows...',
        'Это может занять несколько секунд.',
        'Записи не выбраны.',
        'ВЫ СОБИРАЕТЕСЬ УДАЛИТЬ ЗАПИСИ РЕЕСТРА',
        'Файлы программ НЕ будут удалены.',
        'Будет удалена только запись из списка приложений Windows.',
        'Введите "REMOVER", чтобы продолжить: ',
        'Операция отменена.',
        'Удаление отменено: резервная копия реестра не создана полностью.',
        'Нажмите Enter, чтобы продолжить...',
        'Удаление записей...',
        'Удаляется: {name}',
        '✓ Удалено',
        'Удалено записей: {success}/{total}.',
        'ВЫБОР',
        'Введите номера записей для удаления.',
        'Пример: 1,3,5',
        'Введите ALL, чтобы выбрать все записи.',
        'Введите 0 для отмены.',
        'Выбор: ',
        'Резервная копия создана: \n{path}',
        'Резервная копия неполная: {error}. Записи не будут удалены.',
        '⚠ ВНИМАНИЕ: папка установки ещё существует!',
        'Удаляется только запись реестра...',
        'Отказано в доступе.',
        'Ошибка: {error}')}


BULK_TEXT = {
    "pt-BR": ("REMOVER TODOS OS APLICATIVOS ENCONTRADOS", "Foram encontrados {total} aplicativos provavelmente mortos:", "ATENÇÃO:", "Esta opção removerá TODAS as entradas classificadas como MORTO.", "Ela NÃO remove os arquivos dos programas.", 'Digite "REMOVER TODOS" para continuar: ', "Nenhum aplicativo encontrado.", "Sem permissão para ler o Registro: {path}", "VERIFICADOR DE APLICATIVOS MORTOS DO WINDOWS"),
    "en": ("REMOVE ALL FOUND APPLICATIONS", "{total} applications were identified as likely inactive:", "WARNING:", "This option removes ALL entries classified as DEAD.", "It does NOT remove the program files.", 'Type "REMOVER TODOS" to continue: ', "No applications found.", "Permission denied while reading Registry path: {path}", "WINDOWS APPLICATION DEAD-ENTRY CHECKER"),
    "es": ("ELIMINAR TODAS LAS APLICACIONES ENCONTRADAS", "Se encontraron {total} aplicaciones probablemente inactivas:", "ATENCIÓN:", "Esta opción eliminará TODAS las entradas clasificadas como INACTIVAS.", "NO elimina los archivos de los programas.", 'Escriba "REMOVER TODOS" para continuar: ', "No se encontraron aplicaciones.", "Sin permiso para leer la ruta del Registro: {path}", "VERIFICADOR DE APLICACIONES INACTIVAS DE WINDOWS"),
    "fr": ("SUPPRIMER TOUTES LES APPLICATIONS TROUVÉES", "{total} applications probablement inactives ont été trouvées :", "ATTENTION :", "Cette option supprime TOUTES les entrées classées comme INACTIVES.", "Les fichiers des programmes ne sont PAS supprimés.", 'Saisissez "REMOVER TODOS" pour continuer : ', "Aucune application trouvée.", "Accès refusé à cette clé du Registre : {path}", "VÉRIFICATEUR DES ENTRÉES D’APPLICATIONS INACTIVES WINDOWS"),
    "de": ("ALLE GEFUNDENEN ANWENDUNGEN ENTFERNEN", "{total} wahrscheinlich inaktive Anwendungen gefunden:", "ACHTUNG:", "Diese Option entfernt ALLE als INAKTIV eingestuften Einträge.", "Die Programmdateien werden NICHT entfernt.", 'Geben Sie "REMOVER TODOS" ein, um fortzufahren: ', "Keine Anwendungen gefunden.", "Kein Zugriff auf diesen Registrierungspfad: {path}", "PRÜFUNG INAKTIVER WINDOWS-ANWENDUNGSEINTRÄGE"),
    "it": ("RIMUOVI TUTTE LE APPLICAZIONI TROVATE", "Trovate {total} applicazioni probabilmente inattive:", "ATTENZIONE:", "Questa opzione rimuove TUTTE le voci classificate come INATTIVE.", "I file dei programmi NON vengono rimossi.", 'Digita "REMOVER TODOS" per continuare: ', "Nessuna applicazione trovata.", "Accesso negato a questo percorso del Registro: {path}", "VERIFICA DELLE VOCI DI APPLICAZIONI INATTIVE DI WINDOWS"),
    "ja": ("見つかったアプリをすべて削除", "無効の可能性があるアプリが {total} 件見つかりました:", "注意:", "この操作では、無効と分類された項目をすべて削除します。", "プログラムのファイルは削除されません。", '続行するには "REMOVER TODOS" と入力してください: ', "アプリが見つかりませんでした。", "レジストリ パスを読み取る権限がありません: {path}", "Windows アプリ登録状態チェッカー"),
    "ko": ("찾은 앱 모두 제거", "비활성 상태일 가능성이 있는 앱 {total}개를 찾았습니다:", "주의:", "이 옵션은 비활성으로 분류된 항목을 모두 제거합니다.", "프로그램 파일은 제거되지 않습니다.", '계속하려면 "REMOVER TODOS"를 입력하세요: ', "앱을 찾지 못했습니다.", "레지스트리 경로를 읽을 권한이 없습니다: {path}", "Windows 앱 등록 상태 검사기"),
    "zh-CN": ("删除所有找到的应用", "找到 {total} 个可能无效的应用：", "注意：", "此选项将删除所有被归类为无效的条目。", "不会删除程序文件。", '输入 "REMOVER TODOS" 以继续：', "未找到应用。", "无权读取此注册表路径：{path}", "Windows 应用失效条目检查器"),
    "ru": ("УДАЛИТЬ ВСЕ НАЙДЕННЫЕ ПРИЛОЖЕНИЯ", "Найдено потенциально неактивных приложений: {total}", "ВНИМАНИЕ:", "Этот вариант удалит ВСЕ записи, отмеченные как НЕАКТИВНЫЕ.", "Файлы программ НЕ удаляются.", 'Введите "REMOVER TODOS", чтобы продолжить: ', "Приложения не найдены.", "Нет доступа к этому разделу реестра: {path}", "ПРОВЕРКА НЕАКТИВНЫХ ЗАПИСЕЙ ПРИЛОЖЕНИЙ WINDOWS"),
}

DETAIL_LABELS = {
    "pt-BR": ("Pasta", "Registro", "Chave", "Motivo", "APLICATIVOS SUSPEITOS"),
    "en": ("Folder", "Registry", "Key", "Reason", "SUSPICIOUS APPLICATIONS"),
    "es": ("Carpeta", "Registro", "Clave", "Motivo", "APLICACIONES SOSPECHOSAS"),
    "fr": ("Dossier", "Registre", "Clé", "Motif", "APPLICATIONS SUSPECTES"),
    "de": ("Ordner", "Registrierung", "Schlüssel", "Grund", "VERDÄCHTIGE ANWENDUNGEN"),
    "it": ("Cartella", "Registro", "Chiave", "Motivo", "APPLICAZIONI SOSPETTE"),
    "ja": ("フォルダー", "レジストリ", "キー", "理由", "疑わしいアプリ"),
    "ko": ("폴더", "레지스트리", "키", "이유", "의심 앱"),
    "zh-CN": ("文件夹", "注册表", "项", "原因", "可疑应用"),
    "ru": ("Папка", "Реестр", "Раздел", "Причина", "ПОДОЗРИТЕЛЬНЫЕ ПРИЛОЖЕНИЯ"),
}


MENU_STATUS_TEXT = {
    "pt-BR": ("Nenhum aplicativo suspeito encontrado.", "Nenhuma entrada morta encontrada.", "Nenhum morto para selecionar.", "Opção inválida.", "Saindo..."),
    "en": ("No suspicious applications found.", "No inactive entries found.", "No inactive entries to select.", "Invalid option.", "Exiting..."),
    "es": ("No se encontraron aplicaciones sospechosas.", "No se encontraron entradas inactivas.", "No hay entradas inactivas para seleccionar.", "Opción no válida.", "Saliendo..."),
    "fr": ("Aucune application suspecte trouvée.", "Aucune entrée inactive trouvée.", "Aucune entrée inactive à sélectionner.", "Option invalide.", "Fermeture..."),
    "de": ("Keine verdächtigen Apps gefunden.", "Keine inaktiven Einträge gefunden.", "Keine inaktiven Einträge zur Auswahl.", "Ungültige Option.", "Wird beendet..."),
    "it": ("Nessuna applicazione sospetta trovata.", "Nessuna voce inattiva trovata.", "Nessuna voce inattiva da selezionare.", "Opzione non valida.", "Uscita..."),
    "ja": ("疑わしいアプリは見つかりませんでした。", "無効な項目は見つかりませんでした。", "選択できる無効な項目はありません。", "無効な選択です。", "終了します..."),
    "ko": ("의심스러운 앱을 찾지 못했습니다.", "비활성 항목을 찾지 못했습니다.", "선택할 비활성 항목이 없습니다.", "잘못된 옵션입니다.", "종료 중..."),
    "zh-CN": ("未找到可疑应用。", "未找到无效条目。", "没有可供选择的无效条目。", "选项无效。", "正在退出..."),
    "ru": ("Подозрительные приложения не найдены.", "Неактивные записи не найдены.", "Нет неактивных записей для выбора.", "Неверный пункт меню.", "Выход..."),
}


def detect_ui_language():
    """Map the Windows UI language to one of the ten supported locales."""
    try:
        lang_id = ctypes.windll.kernel32.GetUserDefaultUILanguage()
        primary = lang_id & 0x03FF
    except (AttributeError, OSError):
        return "pt-BR"
    if primary == 0x04 and (lang_id & 0xFC00) not in (0x0800, 0x1000):
        return "pt-BR"
    return {
        0x16: "pt-BR", 0x09: "en", 0x0A: "es", 0x0C: "fr",
        0x07: "de", 0x10: "it", 0x11: "ja", 0x12: "ko",
        0x04: "zh-CN", 0x19: "ru",
    }.get(primary, "pt-BR")


def action_text(index, **values):
    """Return a localized operation message while preserving technical tokens."""
    language = detect_ui_language()
    message = ACTION_TEXT[language][index]
    if index == 10:
        message = message.replace("REMOVER", REMOVAL_CONFIRMATIONS[language])
    return message.format(**values)


def bulk_text(index, **values):
    language = detect_ui_language()
    message = BULK_TEXT[language][index]
    if index == 5:
        message = message.replace("REMOVER TODOS", BULK_CONFIRMATIONS[language])
    return message.format(**values)


REMOVAL_CONFIRMATIONS = {
    "pt-BR": "REMOVER", "en": "REMOVE", "es": "ELIMINAR",
    "fr": "SUPPRIMER", "de": "ENTFERNEN", "it": "RIMUOVI",
    "ja": "削除", "ko": "삭제", "zh-CN": "删除", "ru": "УДАЛИТЬ",
}
BULK_CONFIRMATIONS = {
    "pt-BR": "REMOVER TODOS", "en": "REMOVE ALL", "es": "ELIMINAR TODO",
    "fr": "TOUT SUPPRIMER", "de": "ALLE ENTFERNEN", "it": "RIMUOVI TUTTO",
    "ja": "すべて削除", "ko": "모두 삭제", "zh-CN": "全部删除", "ru": "УДАЛИТЬ ВСЕ",
}


def menu_status_text(index):
    return MENU_STATUS_TEXT[detect_ui_language()][index]


def show_session_header():
    language = detect_ui_language()
    labels = SESSION_LABELS[language]
    started = datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")
    print(C.CYAN + "=" * 78 + C.RESET)
    print(C.BOLD + "ClearDeath App Detector" + C.RESET)
    print(f"{labels[0]}: 1.0.0")
    print(f"{labels[1]}: {started}")
    print(f"{labels[2]}: {language}")
    print(C.CYAN + "=" * 78 + C.RESET)


def enable_colors():
    """
    Ativa ANSI colors no Windows moderno.
    """
    if os.name != "nt":
        return

    try:
        kernel32 = ctypes.windll.kernel32
        handle = kernel32.GetStdHandle(-11)

        mode = ctypes.c_ulong()

        if kernel32.GetConsoleMode(handle, ctypes.byref(mode)):
            kernel32.SetConsoleMode(handle, mode.value | 0x0004)

    except Exception:
        pass


# ============================================================
# ADMIN
# ============================================================

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception:
        return False


def restart_as_admin():
    """
    Reinicia o próprio script como administrador.
    """
    if is_admin():
        return True

    print()
    print(C.YELLOW + action_text(0) + C.RESET)
    print(action_text(1))

    try:
        script = os.path.abspath(sys.argv[0])

        params = " ".join(
            f'"{arg}"'
            for arg in sys.argv[1:]
        )

        result = ctypes.windll.shell32.ShellExecuteW(
            None,
            "runas",
            sys.executable,
            f'"{script}" {params}',
            None,
            1
        )

        if result <= 32:
            print(C.RED + action_text(2) + C.RESET)
            return False

        sys.exit(0)

    except Exception as e:
        print(C.RED + action_text(3, error=e) + C.RESET)
        return False


# ============================================================
# REGISTRO
# ============================================================

def read_value(key, name):
    try:
        value, _ = winreg.QueryValueEx(key, name)
        return value
    except (FileNotFoundError, OSError):
        return None


# ============================================================
# CAMINHOS
# ============================================================

def expand_path(path):
    """
    Expande variáveis como:
    %ProgramFiles%
    %USERPROFILE%
    %LOCALAPPDATA%
    """
    if not path:
        return None

    path = str(path).strip()

    path = os.path.expandvars(path)

    # Variáveis comuns que às vezes não são expandidas
    replacements = {
        "%ProgramFiles%": os.environ.get("ProgramFiles", ""),
        "%ProgramFiles(x86)%": os.environ.get("ProgramFiles(x86)", ""),
        "%ProgramData%": os.environ.get("ProgramData", ""),
        "%AppData%": os.environ.get("APPDATA", ""),
        "%LocalAppData%": os.environ.get("LOCALAPPDATA", ""),
        "%UserProfile%": os.environ.get("USERPROFILE", ""),
    }

    for key, value in replacements.items():
        if value:
            path = path.replace(key, value)

    return path


def remove_outer_quotes(path):
    if not path:
        return path

    path = path.strip()

    if len(path) >= 2:
        if path[0] == '"' and path[-1] == '"':
            return path[1:-1]

    return path


def extract_executable(command):
    """
    Extrai corretamente o executável de comandos como:

    "C:\\Program Files\\Programa\\uninstall.exe" /S

    C:\\Programa\\uninstall.exe /quiet

    C:\\Windows\\System32\\msiexec.exe /X {GUID}

    Ao contrário do script anterior, NÃO usamos split()
    para simplesmente pegar a primeira palavra.
    """

    if not command:
        return None

    command = str(command).strip()

    if not command:
        return None

    # Caso esteja entre aspas
    if command.startswith('"'):
        end_quote = command.find('"', 1)

        if end_quote != -1:
            exe = command[1:end_quote]
            return expand_path(exe)

    # Caso sem aspas.
    #
    # Tentamos encontrar uma extensão executável.
    match = re.search(
        r'(?i)([a-zA-Z]:\\.*?\.(?:exe|com|bat|cmd|msi))(?=\s|$)',
        command
    )

    if match:
        return expand_path(match.group(1))

    # Caso seja apenas o nome do executável
    first = command.split()[0]

    return expand_path(remove_outer_quotes(first))


def executable_name(path):
    if not path:
        return ""

    return os.path.basename(path).lower()


def is_windows_installer(path):
    """
    Detecta msiexec.exe mesmo quando o caminho completo é usado.
    """
    if not path:
        return False

    return executable_name(path) in WINDOWS_INSTALLERS


def path_exists(path):
    if not path:
        return False

    try:
        return os.path.exists(path)
    except Exception:
        return False


def file_exists(path):
    if not path:
        return False

    try:
        return os.path.isfile(path)
    except Exception:
        return False


# ============================================================
# DISPLAY ICON
# ============================================================

def extract_icon_path(display_icon):
    """
    DisplayIcon pode ser:

    C:\\Programa\\programa.exe
    C:\\Programa\\programa.exe,0
    "C:\\Programa\\programa.exe"
    """

    if not display_icon:
        return None

    value = str(display_icon).strip()

    # Remove ",0", ",1", etc.
    value = re.sub(r',-?\d+\s*$', '', value)

    value = remove_outer_quotes(value)

    return expand_path(value)


# ============================================================
# ANALISAR APLICATIVO
# ============================================================

def analyze_application(app):
    name = app["name"]

    install_location = app["install_location"]
    uninstall_string = app["uninstall_string"]
    quiet_uninstall = app["quiet_uninstall"]
    display_icon = app["display_icon"]

    evidence = []

    # --------------------------------------------------------
    # 1. InstallLocation existe
    # --------------------------------------------------------

    if install_location:

        if path_exists(install_location):

            evidence.append(
                "A pasta de instalação existe."
            )

            return {
                **app,
                "status": "OK",
                "reason": ANALYSIS_REASONS[detect_ui_language()][0],
                "evidence": evidence,
            }

        else:

            evidence.append(
                "A pasta de instalação NÃO existe."
            )

    # --------------------------------------------------------
    # 2. DisplayIcon
    # --------------------------------------------------------

    icon_path = extract_icon_path(display_icon)

    if icon_path:

        if file_exists(icon_path):

            evidence.append(
                f"Executável do ícone encontrado: {icon_path}"
            )

            return {
                **app,
                "status": "OK",
                "reason": ANALYSIS_REASONS[detect_ui_language()][1],
                "evidence": evidence,
            }

        else:

            evidence.append(
                f"Executável do ícone não encontrado: {icon_path}"
            )

    # --------------------------------------------------------
    # 3. QuietUninstall
    # --------------------------------------------------------

    quiet_exe = extract_executable(quiet_uninstall)

    if quiet_exe:

        if is_windows_installer(quiet_exe):

            evidence.append(
                "Desinstalador utiliza Windows Installer."
            )

        elif file_exists(quiet_exe):

            evidence.append(
                f"Desinstalador encontrado: {quiet_exe}"
            )

            return {
                **app,
                "status": "OK",
                "reason": ANALYSIS_REASONS[detect_ui_language()][2],
                "evidence": evidence,
            }

        else:

            evidence.append(
                f"Desinstalador não encontrado: {quiet_exe}"
            )

    # --------------------------------------------------------
    # 4. UninstallString
    # --------------------------------------------------------

    uninstall_exe = extract_executable(uninstall_string)

    if uninstall_exe:

        if is_windows_installer(uninstall_exe):

            evidence.append(
                "Usa MsiExec.exe; entrada MSI não será marcada como morta."
            )

            return {
                **app,
                "status": "SUSPEITO",
                "reason": ANALYSIS_REASONS[detect_ui_language()][3],
                "evidence": evidence,
            }

        if file_exists(uninstall_exe):

            evidence.append(
                f"Desinstalador encontrado: {uninstall_exe}"
            )

            return {
                **app,
                "status": "OK",
                "reason": ANALYSIS_REASONS[detect_ui_language()][2],
                "evidence": evidence,
            }

        else:

            evidence.append(
                f"Desinstalador não encontrado: {uninstall_exe}"
            )

    # --------------------------------------------------------
    # 5. Não temos evidência suficiente
    # --------------------------------------------------------

    #
    # IMPORTANTE:
    #
    # Não vamos marcar automaticamente como morto apenas
    # porque faltou uma informação.
    #

    if install_location and not path_exists(install_location):

        if uninstall_string or quiet_uninstall or display_icon:

            return {
                **app,
                "status": "MORTO",
                "reason": ANALYSIS_REASONS[detect_ui_language()][4],
                "evidence": evidence,
            }

    return {
        **app,
        "status": "SUSPEITO",
        "reason": ANALYSIS_REASONS[detect_ui_language()][5],
        "evidence": evidence,
    }


# ============================================================
# LER REGISTRO
# ============================================================

def scan_registry():

    applications = []

    for root, registry_path, root_name in REGISTRY_PATHS:

        try:

            with winreg.OpenKey(
                root,
                registry_path,
                0,
                winreg.KEY_READ
            ) as uninstall_key:

                subkey_count = winreg.QueryInfoKey(uninstall_key)[0]

                for index in range(subkey_count):

                    try:

                        subkey_name = winreg.EnumKey(
                            uninstall_key,
                            index
                        )

                        with winreg.OpenKey(
                            uninstall_key,
                            subkey_name,
                            0,
                            winreg.KEY_READ
                        ) as app_key:

                            display_name = read_value(
                                app_key,
                                "DisplayName"
                            )

                            if not display_name:
                                continue

                            install_location = read_value(
                                app_key,
                                "InstallLocation"
                            )

                            uninstall_string = read_value(
                                app_key,
                                "UninstallString"
                            )

                            quiet_uninstall = read_value(
                                app_key,
                                "QuietUninstallString"
                            )

                            display_icon = read_value(
                                app_key,
                                "DisplayIcon"
                            )

                            app = {
                                "name": str(display_name),

                                "root": root,

                                "root_name": root_name,

                                "registry_path": registry_path,

                                "key": subkey_name,

                                "install_location":
                                    expand_path(install_location),

                                "uninstall_string":
                                    uninstall_string,

                                "quiet_uninstall":
                                    quiet_uninstall,

                                "display_icon":
                                    display_icon,
                            }

                            result = analyze_application(app)

                            applications.append(result)

                    except OSError:
                        continue

        except PermissionError:

            print(
                C.YELLOW +
                bulk_text(7, path=registry_path) +
                C.RESET
            )

        except OSError:
            continue

    return applications


# ============================================================
# STATUS
# ============================================================

def status_text(status):
    labels = RESULT_LABELS[detect_ui_language()]
    if status == "OK":
        return C.GREEN + f"[✓] {labels[6]}" + C.RESET
    if status == "MORTO":
        return C.RED + f"[✗] {labels[7]}" + C.RESET
    return C.YELLOW + f"[?] {labels[8]}" + C.RESET


# ============================================================
# MOSTRAR RESULTADO
# ============================================================

def show_results(apps):
    labels = RESULT_LABELS[detect_ui_language()]
    detail = DETAIL_LABELS[detect_ui_language()]
    print()
    print(C.BOLD + "=" * 78 + C.RESET)
    print(C.BOLD + f"             {labels[0]}" + C.RESET)
    print(C.BOLD + "=" * 78 + C.RESET)

    ok = sum(
        1 for app in apps
        if app["status"] == "OK"
    )

    dead = sum(
        1 for app in apps
        if app["status"] == "MORTO"
    )

    suspicious = sum(
        1 for app in apps
        if app["status"] == "SUSPEITO"
    )

    print()
    print(f"{labels[1]} : {len(apps)}")
    print(C.GREEN + f"{labels[6]:<16}: {ok}" + C.RESET)
    print(C.RED + f"{labels[2]:<16}: {dead}" + C.RESET)
    print(C.YELLOW + f"{labels[3]:<16}: {suspicious}" + C.RESET)
    print()

    # --------------------------------------------------------
    # MORTOS
    # --------------------------------------------------------

    dead_apps = [
        app for app in apps
        if app["status"] == "MORTO"
    ]

    if dead_apps:

        print()
        print(
            C.RED +
            C.BOLD +
            labels[4] +
            C.RESET
        )

        print("-" * 78)

        for number, app in enumerate(dead_apps, 1):

            print(
                C.RED +
                f"[{number}] {app['name']}" +
                C.RESET
            )

            if app["install_location"]:
                print(
                    f"    {detail[0]}: {app['install_location']}"
                )

            print(
                f"    {detail[1]}: {app['root_name']}"
            )

            print(
                f"    {detail[2]}: {app['key']}"
            )

            print(
                f"    {detail[3]}: {app['reason']}"
            )

            print()

    else:

        print(
            C.GREEN +
            labels[5] +
            C.RESET
        )

    return dead_apps


# ============================================================
# BACKUP
# ============================================================

def backup_registry(dead_apps):
    """Export every selected key; fail closed if any export is incomplete."""
    if not dead_apps:
        return None
    base_dir = os.environ.get("LOCALAPPDATA") or os.path.join(os.path.expanduser("~"), "AppData", "Local")
    backup_dir = os.path.join(base_dir, "Emertels", "ClearDeath", "Backups")
    os.makedirs(backup_dir, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    backup_file = os.path.join(backup_dir, f"backup_apps_{stamp}.reg")
    temp_files = []
    try:
        with open(backup_file, "w", encoding="utf-16") as output:
            output.write("Windows Registry Editor Version 5.00\n\n")
            for index, app in enumerate(dead_apps, 1):
                if app["root_name"] == "HKLM 64-bit":
                    root = "HKEY_LOCAL_MACHINE"
                    path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
                elif app["root_name"] == "HKLM 32-bit":
                    root = "HKEY_LOCAL_MACHINE"
                    path = r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
                else:
                    root = "HKEY_CURRENT_USER"
                    path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
                full_path = root + "\\" + path + "\\" + app["key"]
                temp_file = backup_file + f".{index}.tmp"
                temp_files.append(temp_file)
                result = subprocess.run(
                    ["reg", "export", full_path, temp_file, "/y"],
                    capture_output=True, text=True,
                    creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0)
                )
                if result.returncode != 0 or not os.path.isfile(temp_file):
                    raise RuntimeError(f"Falha ao exportar a chave: {full_path}")
                with open(temp_file, "r", encoding="utf-16") as exported:
                    content = exported.read()
                header = "Windows Registry Editor Version 5.00"
                if header not in content or "[" not in content:
                    raise RuntimeError(f"Exportação inválida para a chave: {full_path}")
                output.write(content.replace(header, "").strip() + "\n\n")
        for temp_file in temp_files:
            if os.path.exists(temp_file):
                os.remove(temp_file)
        print(C.GREEN + action_text(24, path=backup_file) + C.RESET)
        return backup_file
    except Exception as exc:
        for temp_file in temp_files:
            try:
                os.remove(temp_file)
            except OSError:
                pass
        try:
            os.remove(backup_file)
        except OSError:
            pass
        print(C.RED + action_text(25, error=exc) + C.RESET)
        return None

# ============================================================
# EXCLUIR CHAVE
# ============================================================

def delete_registry_key(app):

    try:

        root = app["root"]

        full_path = (
            app["registry_path"] +
            "\\" +
            app["key"]
        )

        # Verifica se a pasta de instalação ainda existe
        if app["install_location"] and os.path.exists(app["install_location"]):
            print(C.YELLOW + action_text(26) + C.RESET)
            print("    " + action_text(27))

        winreg.DeleteKey(
            root,
            full_path
        )

        return True

    except FileNotFoundError:

        return True

    except PermissionError:

        print(
            C.RED +
            "    " + action_text(28) +
            C.RESET
        )

        return False

    except OSError as e:

        print(
            C.RED +
            "    " + action_text(29, error=e) +
            C.RESET
        )

        return False


# ============================================================
# LOG DE OPERAÇÕES
# ============================================================

def log_removal(app):
    """Write a removal record to the user's local application data."""
    base_dir = os.environ.get("LOCALAPPDATA") or os.path.join(os.path.expanduser("~"), "AppData", "Local")
    log_dir = os.path.join(base_dir, "Emertels", "ClearDeath")
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "removals.log")
    try:
        with open(log_file, "a", encoding="utf-8") as f:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"{timestamp} - Removed: {app['name']} ({app['key']})\n")
            if app["install_location"]:
                f.write(f"    Install path: {app['install_location']}\n")
            f.write(f"    Registry: {app['root_name']}\n\n")
    except OSError:
        pass

# ============================================================
# REMOVER
# ============================================================

def remove_apps(apps):

    if not apps:
        print()
        print(action_text(6))
        return

    print()
    print(C.RED + C.BOLD + "=" * 78 + C.RESET)
    print(
        C.RED +
        action_text(7) +
        C.RESET
    )
    print(C.RED + C.BOLD + "=" * 78 + C.RESET)

    print()

    for app in apps:

        print(
            C.RED +
            f"- {app['name']}" +
            C.RESET
        )

    print()

    print(
        C.YELLOW +
        action_text(8) +
        C.RESET
    )

    print(
        action_text(9)
    )

    print()

    confirmation = input(
        action_text(10)
    ).strip()

    if confirmation != REMOVAL_CONFIRMATIONS[detect_ui_language()]:

        print()
        print(
            C.YELLOW +
            action_text(11) +
            C.RESET
        )

        return

    # Stop safely unless every selected key has a complete registry export.
    backup_path = backup_registry(apps)
    if not backup_path:
        print(C.RED + action_text(12) + C.RESET)
        input(action_text(13))
        return

    print()
    print(C.CYAN + action_text(14) + C.RESET)
    print()

    success = 0

    for app in apps:

        print(
            action_text(15, name=app["name"])
        )

        if delete_registry_key(app):

            log_removal(app)

            print(
                C.GREEN +
                "    " + action_text(16) +
                C.RESET
            )

            success += 1

        print()

    print(
        C.GREEN +
        C.BOLD +
        action_text(17, success=success, total=len(apps)) +
        C.RESET
    )


# ============================================================
# SELECIONAR
# ============================================================

def select_dead_apps(dead_apps):

    if not dead_apps:
        return []

    print()
    print(C.BOLD + "=" * 78 + C.RESET)
    print(action_text(18))
    print(C.BOLD + "=" * 78 + C.RESET)

    print()
    print(
        action_text(19)
    )

    print(
        action_text(20)
    )

    print(
        action_text(21)
    )

    print(
        action_text(22)
    )

    print()

    for number, app in enumerate(dead_apps, 1):

        print(
            f"{number:3} - {app['name']}"
        )

    print()

    answer = input(
        action_text(23)
    ).strip()

    if answer == "0":
        return []

    if answer.upper() == "ALL":

        return dead_apps

    selected = []

    parts = answer.split(",")

    for part in parts:

        part = part.strip()

        try:

            number = int(part)

            if 1 <= number <= len(dead_apps):

                selected.append(
                    dead_apps[number - 1]
                )

        except ValueError:
            pass

    # Remover duplicados mantendo ordem
    unique = []

    seen = set()

    for app in selected:

        identifier = (
            app["root_name"],
            app["key"]
        )

        if identifier not in seen:

            seen.add(identifier)

            unique.append(app)

    return unique


# ============================================================
# MENU
# ============================================================

def menu(apps, dead_apps):
    labels = MENU_TEXT[detect_ui_language()]
    while True:
        print()
        print(C.BOLD + "=" * 78 + C.RESET)
        print(C.BOLD + labels[0] + C.RESET)
        print(C.BOLD + "=" * 78 + C.RESET)
        print()
        print("1 - " + labels[1])
        print("2 - " + labels[2])
        print("3 - " + labels[3])
        print("4 - " + labels[4])
        print("5 - " + labels[5])
        print()
        choice = input(labels[6]).strip()
        
        # ----------------------------------------------------
        # 1 - MORTOS
        # ----------------------------------------------------
        
        if choice == "1":
            show_results(apps)
        
        # ----------------------------------------------------
        # 2 - SUSPEITOS
        # ----------------------------------------------------
        
        elif choice == "2":
            suspicious = [
                app for app in apps
                if app["status"] == "SUSPEITO"
            ]
            
            if not suspicious:
                print()
                print(C.GREEN + menu_status_text(0) + C.RESET)
                input("\n" + action_text(13))
                continue
            
            print()
            print(C.YELLOW + C.BOLD + DETAIL_LABELS[detect_ui_language()][4] + C.RESET)
            print("-" * 78)
            
            for number, app in enumerate(suspicious, 1):
                print(
                    C.YELLOW +
                    f"[{number}] {app['name']}" +
                    C.RESET
                )
                print(
                    f"    {DETAIL_LABELS[detect_ui_language()][3]}: {app['reason']}"
                )
                if app["install_location"]:
                    print(
                        f"    {DETAIL_LABELS[detect_ui_language()][0]}: {app['install_location']}"
                    )
                print()
            
            input("\n" + action_text(13))
        
        # ----------------------------------------------------
        # 3 - REMOVER SELECIONADOS
        # ----------------------------------------------------
        
        elif choice == "3":
            selected = select_dead_apps(dead_apps)
            remove_apps(selected)
            input("\n" + action_text(13))
        
        # ----------------------------------------------------
        # 4 - REMOVER TODOS OS MORTOS
        # ----------------------------------------------------
        
        elif choice == "4":
            if not dead_apps:
                print()
                print(
                    C.GREEN +
                    menu_status_text(1) +
                    C.RESET
                )
                input(
                    "\n" + action_text(13)
                )
                continue
            
            print()
            print(
                C.RED +
                C.BOLD +
                "=" * 78 +
                C.RESET
            )
            print(
                C.RED + C.BOLD + bulk_text(0) + C.RESET
            )
            print(
                C.RED +
                C.BOLD +
                "=" * 78 +
                C.RESET
            )
            print()
            print(
                bulk_text(1, total=len(dead_apps))
            )
            print()
            
            for app in dead_apps:
                print(
                    C.RED +
                    f"  ✗ {app['name']}" +
                    C.RESET
                )
            
            print()
            print(
                C.YELLOW +
                bulk_text(2) +
                C.RESET
            )
            print(
                bulk_text(3)
            )
            print(
                bulk_text(4)
            )
            print()
            
            confirmation = input(
                bulk_text(5)
            ).strip()
            
            if confirmation != BULK_CONFIRMATIONS[detect_ui_language()]:
                print()
                print(
                    C.YELLOW +
                    action_text(11) +
                    C.RESET
                )
                input(
                    "\n" + action_text(13)
                )
                continue
            
            remove_apps(dead_apps)
            input(
                "\n" + action_text(13)
            )
        
        # ----------------------------------------------------
        # 5 - SAIR
        # ----------------------------------------------------
        
        elif choice == "5":
            print()
            print(menu_status_text(4))
            break
        
        # ----------------------------------------------------
        # OPÇÃO INVÁLIDA
        # ----------------------------------------------------
        
        else:
            print(
                C.YELLOW +
                menu_status_text(3) +
                C.RESET
            )
            input("\n" + action_text(13))


# ============================================================
# MAIN
# ============================================================

def main():

    enable_colors()

    print()
    print(C.BOLD + "=" * 78 + C.RESET)

    print(
        C.BOLD +
        "       " + bulk_text(8) +
        C.RESET
    )

    print(C.BOLD + "=" * 78 + C.RESET)

    print()

    if not restart_as_admin():
        return

    show_session_header()

    print(
        C.CYAN +
        action_text(4) +
        C.RESET
    )

    print(
        action_text(5)
    )

    apps = scan_registry()

    if not apps:

        print()
        print(
            C.YELLOW +
            bulk_text(6) +
            C.RESET
        )

        return

    dead_apps = show_results(apps)

    menu(
        apps,
        dead_apps
    )


# ============================================================
# EXECUTAR
# ============================================================

if __name__ == "__main__":
    main()








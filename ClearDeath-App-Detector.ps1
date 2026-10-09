# ============================================================
# VERIFICADOR DE APLICATIVOS MORTOS DO WINDOWS (POWERSHELL)
# ============================================================
. "$PSScriptRoot\Session-Header.ps1"

$script:ClearDeathUi = @{
    'pt-BR' = @('MENU','Mostrar novamente os mortos','Ver suspeitos','Selecionar entradas para remover','Remover TODOS os encontrados','Sair','Escolha','RESULTADO DA ANÁLISE','Total analisado','MORTOS','SUSPEITOS','ENTRADAS PROVAVELMENTE MORTAS','Nenhuma entrada foi confirmada como morta.','Nenhum aplicativo suspeito encontrado.','Nenhum morto encontrado.','Nenhum morto para selecionar.','Opção inválida.','Saindo...','Seleção')
    'en' = @('MENU','Show dead entries again','View suspicious entries','Select entries to remove','Remove ALL found entries','Exit','Choose','ANALYSIS RESULTS','Total analyzed','DEAD','SUSPICIOUS','PROBABLY DEAD ENTRIES','No entries were confirmed as dead.','No suspicious applications found.','No dead entries found.','No dead entries to select.','Invalid option.','Exiting...','Selection')
    'es' = @('MENÚ','Mostrar de nuevo los inactivos','Ver sospechosos','Seleccionar entradas para eliminar','Eliminar TODAS las entradas encontradas','Salir','Elija','RESULTADOS DEL ANÁLISIS','Total analizado','INACTIVOS','SOSPECHOSOS','ENTRADAS PROBABLEMENTE INACTIVAS','Ninguna entrada fue confirmada como inactiva.','No se encontraron aplicaciones sospechosas.','No se encontraron entradas inactivas.','No hay entradas inactivas para seleccionar.','Opción no válida.','Saliendo...','Selección')
    'fr' = @('MENU','Afficher de nouveau les entrées inactives','Voir les éléments suspects','Sélectionner les entrées à supprimer','Supprimer TOUTES les entrées trouvées','Quitter','Choix','RÉSULTATS DE L’’ANALYSE','Total analysé','INACTIFS','SUSPECTS','ENTRÉES PROBABLEMENT INACTIVES','Aucune entrée n’’a été confirmée comme inactive.','Aucune application suspecte trouvée.','Aucune entrée inactive trouvée.','Aucune entrée inactive à sélectionner.','Option invalide.','Fermeture...','Sélection')
    'de' = @('MENÜ','Inaktive Einträge erneut anzeigen','Verdächtige Einträge anzeigen','Einträge zum Entfernen auswählen','ALLE gefundenen Einträge entfernen','Beenden','Auswahl','ANALYSEERGEBNISSE','Insgesamt geprüft','INAKTIV','VERDÄCHTIG','WAHRSCHEINLICH INAKTIVE EINTRÄGE','Kein Eintrag wurde als inaktiv bestätigt.','Keine verdächtigen Apps gefunden.','Keine inaktiven Einträge gefunden.','Keine inaktiven Einträge zur Auswahl.','Ungültige Option.','Wird beendet...','Auswahl')
    'it' = @('MENU','Mostra di nuovo le voci inattive','Visualizza le voci sospette','Seleziona le voci da rimuovere','Rimuovi TUTTE le voci trovate','Esci','Scelta','RISULTATI DELL’’ANALISI','Totale analizzato','INATTIVI','SOSPETTI','VOCI PROBABILMENTE INATTIVE','Nessuna voce è stata confermata come inattiva.','Nessuna applicazione sospetta trovata.','Nessuna voce inattiva trovata.','Nessuna voce inattiva da selezionare.','Opzione non valida.','Uscita...','Selezione')
    'ja' = @('メニュー','無効な項目を再表示','疑わしい項目を見る','削除する項目を選択','見つかった項目をすべて削除','終了','選択','分析結果','分析した合計','無効','疑わしい','無効の可能性がある項目','無効と確認された項目はありません。','疑わしいアプリは見つかりませんでした。','無効な項目は見つかりませんでした。','選択できる無効な項目はありません。','無効な選択です。','終了します...','選択')
    'ko' = @('메뉴','비활성 항목 다시 표시','의심 항목 보기','삭제할 항목 선택','찾은 항목 모두 삭제','종료','선택','분석 결과','분석된 항목','비활성','의심','비활성일 가능성이 있는 항목','비활성으로 확인된 항목이 없습니다.','의심스러운 앱을 찾지 못했습니다.','비활성 항목을 찾지 못했습니다.','선택할 비활성 항목이 없습니다.','잘못된 옵션입니다.','종료 중...','선택')
    'zh-CN' = @('菜单','再次显示无效条目','查看可疑项目','选择要删除的条目','删除所有找到的条目','退出','选择','分析结果','分析总数','无效','可疑','可能无效的条目','没有条目被确认为无效。','未找到可疑应用。','未找到无效条目。','没有可供选择的无效条目。','选项无效。','正在退出...','选择')
    'ru' = @('МЕНЮ','Показать неактивные записи снова','Показать подозрительные записи','Выбрать записи для удаления','Удалить ВСЕ найденные записи','Выход','Выберите','РЕЗУЛЬТАТЫ АНАЛИЗА','Проверено всего','НЕАКТИВНЫЕ','ПОДОЗРИТЕЛЬНЫЕ','ВЕРОЯТНО НЕАКТИВНЫЕ ЗАПИСИ','Не удалось подтвердить ни одной неактивной записи.','Подозрительные приложения не найдены.','Неактивные записи не найдены.','Нет неактивных записей для выбора.','Неверный пункт меню.','Выход...','Выбор')
}
$script:Ui = $script:ClearDeathUi[$script:AppLanguage]

$script:AnalysisReasons = @{
    'pt-BR'=@("Pasta de instalação encontrada.","Executável associado ao aplicativo encontrado.","Desinstalador encontrado.","Usa Windows Installer (MSI).","Pasta de instalação e referências principais não foram encontradas.","Não foi possível confirmar se o aplicativo está instalado.")
    'en'=@("Installation folder found.","Application executable found.","Uninstaller found.","Uses Windows Installer (MSI).","The installation folder and primary references were not found.","Could not confirm whether the application is installed.")
    'es'=@("Se encontró la carpeta de instalación.","Se encontró el ejecutable asociado a la aplicación.","Se encontró el desinstalador.","Usa Windows Installer (MSI).","No se encontraron la carpeta de instalación ni las referencias principales.","No se pudo confirmar si la aplicación está instalada.")
    'fr'=@("Dossier d’’installation trouvé.","Exécutable associé à l’’application trouvé.","Programme de désinstallation trouvé.","Utilise Windows Installer (MSI).","Le dossier d’’installation et les références principales sont introuvables.","Impossible de confirmer si l’’application est installée.")
    'de'=@("Installationsordner gefunden.","Zugehörige Anwendungsdatei gefunden.","Deinstallationsprogramm gefunden.","Verwendet Windows Installer (MSI).","Installationsordner und wichtige Verweise wurden nicht gefunden.","Der Installationsstatus der Anwendung konnte nicht bestätigt werden.")
    'it'=@("Cartella di installazione trovata.","Eseguibile associato all’’applicazione trovato.","Programma di disinstallazione trovato.","Usa Windows Installer (MSI).","Cartella di installazione e riferimenti principali non trovati.","Impossibile confermare se l’’applicazione è installata.")
    'ja'=@("インストールフォルダーが見つかりました。","アプリに関連付けられた実行ファイルが見つかりました。","アンインストーラーが見つかりました。","Windows Installer (MSI) を使用しています。","インストールフォルダーと主な参照先が見つかりません。","アプリがインストールされているか確認できませんでした。")
    'ko'=@("설치 폴더를 찾았습니다.","앱과 연결된 실행 파일을 찾았습니다.","제거 프로그램을 찾았습니다.","Windows Installer(MSI)를 사용합니다.","설치 폴더와 주요 참조 항목을 찾을 수 없습니다.","앱의 설치 여부를 확인할 수 없습니다.")
    'zh-CN'=@("已找到安装文件夹。","已找到与应用关联的可执行文件。","已找到卸载程序。","使用 Windows Installer (MSI)。","未找到安装文件夹和主要引用项。","无法确认应用是否已安装。")
    'ru'=@("Папка установки найдена.","Исполняемый файл приложения найден.","Программа удаления найдена.","Используется Windows Installer (MSI).","Папка установки и основные ссылки не найдены.","Не удалось подтвердить, установлено ли приложение.")
}

$script:ClearDeathActions = @{
    'pt-BR'=@('Solicitando privilégios de Administrador...','Criando backup do Registro...','Falha ao exportar uma chave. Nenhuma entrada será removida.','Não foi possível concluir o backup. Nenhuma entrada será removida.','Não foi possível salvar o backup. Nenhuma entrada será removida.','Backup criado em: {0}','Nenhuma entrada selecionada.','VOCÊ ESTÁ PRESTES A REMOVER ENTRADAS DO REGISTRO','Isso NÃO desinstala os arquivos dos programas.','Isso apenas remove a entrada da lista de aplicativos do Windows.','Digite "REMOVER" para continuar','Operação cancelada.','Remoção cancelada porque o backup do Registro não foi concluído.','Removendo entradas...','Removendo: {0}','[OK] Removido','Erro ao remover: {0}','{0}/{1} entradas removidas.','VERIFICADOR DE APLICATIVOS MORTOS DO WINDOWS (POWERSHELL)','Analisando o Registro do Windows... Isso pode levar alguns segundos.','Pasta','Registro','Chave','Motivo','APLICATIVOS SUSPEITOS','Digite os números separados por vírgula (ex.: 1,3) ou ALL para selecionar todos:','A pasta de instalação existe.','A pasta de instalação NÃO existe.','Executável do ícone encontrado: {0}','Executável do ícone não encontrado: {0}','Desinstalador utiliza Windows Installer.','Desinstalador encontrado: {0}','Desinstalador não encontrado: {0}','Usa MsiExec.exe; entrada MSI não será marcada como morta.')
    'en'=@('Requesting Administrator privileges...','Creating registry backup...','Failed to export a key. No entries will be removed.','Backup could not be completed. No entries will be removed.','Backup could not be saved. No entries will be removed.','Backup created at: {0}','No entries selected.','YOU ARE ABOUT TO REMOVE REGISTRY ENTRIES','This does NOT uninstall program files.','This only removes the entry from the Windows apps list.','Type "REMOVE" to continue','Operation cancelled.','Removal cancelled because the registry backup was not completed.','Removing entries...','Removing: {0}','[OK] Removed','Removal error: {0}','{0}/{1} entries removed.','WINDOWS ORPHANED APPLICATION ENTRY SCANNER (POWERSHELL)','Scanning the Windows Registry... This may take a few seconds.','Folder','Registry','Key','Reason','SUSPICIOUS APPLICATIONS','Enter numbers separated by commas (e.g. 1,3), or ALL to select all:','Installation folder exists.','Installation folder does NOT exist.','Icon executable found: {0}','Icon executable not found: {0}','Uninstaller uses Windows Installer.','Uninstaller found: {0}','Uninstaller not found: {0}','Uses MsiExec.exe; the MSI entry will not be marked as orphaned.')
    'es'=@('Solicitando privilegios de administrador...','Creando copia de seguridad del Registro...','No se pudo exportar una clave. No se eliminará ninguna entrada.','No se pudo completar la copia de seguridad. No se eliminará ninguna entrada.','No se pudo guardar la copia de seguridad. No se eliminará ninguna entrada.','Copia de seguridad creada en: {0}','No se seleccionaron entradas.','ESTÁ A PUNTO DE ELIMINAR ENTRADAS DEL REGISTRO','Esto NO desinstala los archivos de los programas.','Esto solo elimina la entrada de la lista de aplicaciones de Windows.','Escriba "ELIMINAR" para continuar','Operación cancelada.','Eliminación cancelada porque no se completó la copia del Registro.','Eliminando entradas...','Eliminando: {0}','[OK] Eliminado','Error al eliminar: {0}','{0}/{1} entradas eliminadas.','ANALIZADOR DE ENTRADAS DE APLICACIONES HUÉRFANAS (POWERSHELL)','Analizando el Registro de Windows... Esto puede tardar unos segundos.','Carpeta','Registro','Clave','Motivo','APLICACIONES SOSPECHOSAS','Escriba números separados por comas (p. ej., 1,3) o ALL para seleccionar todas:','La carpeta de instalación existe.','La carpeta de instalación NO existe.','Ejecutable del icono encontrado: {0}','Ejecutable del icono no encontrado: {0}','El desinstalador usa Windows Installer.','Desinstalador encontrado: {0}','Desinstalador no encontrado: {0}','Usa MsiExec.exe; la entrada MSI no se marcará como inactiva.')
    'fr'=@('Demande des privilèges administrateur...','Création de la sauvegarde du Registre...','Échec de l’’exportation d’’une clé. Aucune entrée ne sera supprimée.','La sauvegarde n’’a pas pu être terminée. Aucune entrée ne sera supprimée.','La sauvegarde n’’a pas pu être enregistrée. Aucune entrée ne sera supprimée.','Sauvegarde créée dans : {0}','Aucune entrée sélectionnée.','VOUS ÊTES SUR LE POINT DE SUPPRIMER DES ENTRÉES DU REGISTRE','Cela ne désinstalle PAS les fichiers des programmes.','Cela supprime uniquement l’’entrée de la liste des applications Windows.','Saisissez « SUPPRIMER » pour continuer','Opération annulée.','Suppression annulée car la sauvegarde du Registre a échoué.','Suppression des entrées...','Suppression : {0}','[OK] Supprimée','Erreur de suppression : {0}','{0}/{1} entrées supprimées.','ANALYSEUR DES ENTRÉES D’’APPLICATIONS ORPHELINES (POWERSHELL)','Analyse du Registre Windows... Cela peut prendre quelques secondes.','Dossier','Registre','Clé','Motif','APPLICATIONS SUSPECTES','Saisissez les numéros séparés par des virgules (ex. : 1,3) ou ALL pour tout sélectionner :','Le dossier d’’installation existe.','Le dossier d’’installation n’’existe PAS.','Exécutable de l’’icône trouvé : {0}','Exécutable de l’’icône introuvable : {0}','Le désinstalleur utilise Windows Installer.','Désinstalleur trouvé : {0}','Désinstalleur introuvable : {0}','Utilise MsiExec.exe ; l’’entrée MSI ne sera pas marquée comme orpheline.')
    'de'=@('Administratorrechte werden angefordert...','Registrierungssicherung wird erstellt...','Ein Schlüssel konnte nicht exportiert werden. Es werden keine Einträge entfernt.','Sicherung konnte nicht abgeschlossen werden. Es werden keine Einträge entfernt.','Sicherung konnte nicht gespeichert werden. Es werden keine Einträge entfernt.','Sicherung erstellt unter: {0}','Keine Einträge ausgewählt.','SIE SIND IM BEGRIFF, REGISTRIERUNGSEINTRÄGE ZU ENTFERNEN','Dadurch werden Programmdateien NICHT deinstalliert.','Dadurch wird nur der Eintrag aus der Windows-App-Liste entfernt.','Geben Sie "ENTFERNEN" ein, um fortzufahren','Vorgang abgebrochen.','Entfernung abgebrochen, da die Registrierungssicherung nicht erstellt wurde.','Einträge werden entfernt...','Wird entfernt: {0}','[OK] Entfernt','Fehler beim Entfernen: {0}','{0}/{1} Einträge entfernt.','PRÜFUNG VERWAISTER WINDOWS-APP-EINTRÄGE (POWERSHELL)','Windows-Registrierung wird geprüft... Dies kann einige Sekunden dauern.','Ordner','Registrierung','Schlüssel','Grund','VERDÄCHTIGE ANWENDUNGEN','Geben Sie durch Kommas getrennte Nummern (z. B. 1,3) oder ALL ein:','Installationsordner ist vorhanden.','Installationsordner ist NICHT vorhanden.','Icon-Programmdatei gefunden: {0}','Icon-Programmdatei nicht gefunden: {0}','Deinstallationsprogramm verwendet Windows Installer.','Deinstallationsprogramm gefunden: {0}','Deinstallationsprogramm nicht gefunden: {0}','Verwendet MsiExec.exe; der MSI-Eintrag wird nicht als verwaist markiert.')
    'it'=@('Richiesta dei privilegi di amministratore...','Creazione del backup del Registro...','Impossibile esportare una chiave. Non verrà rimossa alcuna voce.','Impossibile completare il backup. Non verrà rimossa alcuna voce.','Impossibile salvare il backup. Non verrà rimossa alcuna voce.','Backup creato in: {0}','Nessuna voce selezionata.','STAI PER RIMUOVERE VOCI DAL REGISTRO','Questo NON disinstalla i file dei programmi.','Questo rimuove solo la voce dall’’elenco delle app di Windows.','Digita "RIMUOVI" per continuare','Operazione annullata.','Rimozione annullata perché il backup del Registro non è stato completato.','Rimozione delle voci...','Rimozione: {0}','[OK] Rimossa','Errore durante la rimozione: {0}','{0}/{1} voci rimosse.','ANALIZZATORE DI VOCI ORFANE DELLE APP WINDOWS (POWERSHELL)','Analisi del Registro di Windows... Potrebbero volerci alcuni secondi.','Cartella','Registro','Chiave','Motivo','APPLICAZIONI SOSPETTE','Inserisci numeri separati da virgole (es. 1,3) oppure ALL per selezionarle tutte:','La cartella di installazione esiste.','La cartella di installazione NON esiste.','Eseguibile dell’’icona trovato: {0}','Eseguibile dell’’icona non trovato: {0}','Il programma di disinstallazione usa Windows Installer.','Programma di disinstallazione trovato: {0}','Programma di disinstallazione non trovato: {0}','Usa MsiExec.exe; la voce MSI non verrà segnalata come orfana.')
    'ja'=@('管理者権限を要求しています...','レジストリのバックアップを作成しています...','キーのエクスポートに失敗しました。項目は削除されません。','バックアップを完了できませんでした。項目は削除されません。','バックアップを保存できませんでした。項目は削除されません。','バックアップの保存先: {0}','項目が選択されていません。','レジストリ項目を削除しようとしています','プログラムのファイルはアンインストールされません。','Windows アプリ一覧から項目のみを削除します。','続行するには「削除」と入力してください','操作をキャンセルしました。','レジストリのバックアップが完了しなかったため削除を中止しました。','項目を削除しています...','削除中: {0}','[OK] 削除済み','削除エラー: {0}','{0}/{1} 件の項目を削除しました。','Windows の孤立したアプリ項目を確認 (PowerShell)','Windows レジストリを確認しています...数秒かかる場合があります。','フォルダー','レジストリ','キー','理由','疑わしいアプリ','カンマ区切りの番号（例: 1,3）または ALL を入力:','インストールフォルダーが存在します。','インストールフォルダーが存在しません。','アイコンの実行ファイルが見つかりました: {0}','アイコンの実行ファイルが見つかりません: {0}','アンインストーラーは Windows Installer を使用します。','アンインストーラーが見つかりました: {0}','アンインストーラーが見つかりません: {0}','MsiExec.exe を使用しています。MSI 項目は孤立として扱いません。')
    'ko'=@('관리자 권한을 요청하는 중...','레지스트리 백업을 만드는 중...','키 내보내기에 실패했습니다. 항목을 삭제하지 않습니다.','백업을 완료할 수 없습니다. 항목을 삭제하지 않습니다.','백업을 저장할 수 없습니다. 항목을 삭제하지 않습니다.','백업 저장 위치: {0}','선택한 항목이 없습니다.','레지스트리 항목을 삭제하려고 합니다','프로그램 파일은 제거되지 않습니다.','Windows 앱 목록에서 항목만 제거합니다.','계속하려면 "삭제"를 입력하세요','작업이 취소되었습니다.','레지스트리 백업이 완료되지 않아 삭제를 취소했습니다.','항목을 삭제하는 중...','삭제 중: {0}','[OK] 삭제됨','삭제 오류: {0}','{0}/{1}개 항목 삭제됨.','Windows 고아 앱 항목 검사기 (PowerShell)','Windows 레지스트리를 검사하는 중... 몇 초 정도 걸릴 수 있습니다.','폴더','레지스트리','키','이유','의심스러운 애플리케이션','쉼표로 구분된 번호(예: 1,3) 또는 ALL을 입력하세요:','설치 폴더가 있습니다.','설치 폴더가 없습니다.','아이콘 실행 파일을 찾았습니다: {0}','아이콘 실행 파일을 찾을 수 없습니다: {0}','제거 프로그램이 Windows Installer를 사용합니다.','제거 프로그램을 찾았습니다: {0}','제거 프로그램을 찾을 수 없습니다: {0}','MsiExec.exe를 사용합니다. MSI 항목은 고아로 표시하지 않습니다.')
    'zh-CN'=@('正在请求管理员权限...','正在创建注册表备份...','无法导出一个项。不会删除任何条目。','无法完成备份。不会删除任何条目。','无法保存备份。不会删除任何条目。','备份已创建于：{0}','未选择任何条目。','即将删除注册表条目','这不会卸载程序文件。','这只会从 Windows 应用列表中删除该条目。','输入“删除”以继续','操作已取消。','注册表备份未完成，已取消删除。','正在删除条目...','正在删除：{0}','[OK] 已删除','删除错误：{0}','已删除 {0}/{1} 个条目。','Windows 孤立应用条目检查器 (PowerShell)','正在扫描 Windows 注册表...这可能需要几秒钟。','文件夹','注册表','项','原因','可疑应用','输入以逗号分隔的编号（例如 1,3）或 ALL 以全选：','安装文件夹存在。','安装文件夹不存在。','找到图标可执行文件：{0}','未找到图标可执行文件：{0}','卸载程序使用 Windows Installer。','找到卸载程序：{0}','未找到卸载程序：{0}','使用 MsiExec.exe；不会将 MSI 条目标记为孤立。')
    'ru'=@('Запрос прав администратора...','Создание резервной копии реестра...','Не удалось экспортировать ключ. Записи не будут удалены.','Не удалось завершить резервное копирование. Записи не будут удалены.','Не удалось сохранить резервную копию. Записи не будут удалены.','Резервная копия создана: {0}','Записи не выбраны.','ВЫ СОБИРАЕТЕСЬ УДАЛИТЬ ЗАПИСИ РЕЕСТРА','Файлы программ НЕ будут удалены.','Будет удалена только запись из списка приложений Windows.','Введите "УДАЛИТЬ" для продолжения','Операция отменена.','Удаление отменено: резервная копия реестра не создана.','Удаление записей...','Удаление: {0}','[OK] Удалено','Ошибка удаления: {0}','Удалено записей: {0}/{1}.','ПРОВЕРКА ОСИРОТЕВШИХ ЗАПИСЕЙ ПРИЛОЖЕНИЙ WINDOWS (POWERSHELL)','Проверка реестра Windows... Это может занять несколько секунд.','Папка','Реестр','Ключ','Причина','ПОДОЗРИТЕЛЬНЫЕ ПРИЛОЖЕНИЯ','Введите номера через запятую (например, 1,3) или ALL для выбора всех:','Папка установки существует.','Папка установки НЕ существует.','Исполняемый файл значка найден: {0}','Исполняемый файл значка не найден: {0}','Деинсталлятор использует Windows Installer.','Деинсталлятор найден: {0}','Деинсталлятор не найден: {0}','Используется MsiExec.exe; запись MSI не будет отмечена как осиротевшая.')
}
$script:Action = $script:ClearDeathActions[$script:AppLanguage]
$script:ConfirmToken = @{
    'pt-BR'='REMOVER'; 'en'='REMOVE'; 'es'='ELIMINAR'; 'fr'='SUPPRIMER'; 'de'='ENTFERNEN';
    'it'='RIMUOVI'; 'ja'='削除'; 'ko'='삭제'; 'zh-CN'='删除'; 'ru'='УДАЛИТЬ'
}[$script:AppLanguage]
$script:EvidenceText = @{
    'pt-BR'=@('A pasta de instalação existe.','A pasta de instalação NÃO existe.','Executável do ícone encontrado: {0}','Executável do ícone não encontrado: {0}','Desinstalador utiliza Windows Installer.','Desinstalador encontrado: {0}','Desinstalador não encontrado: {0}','Usa MsiExec.exe; entrada MSI não será marcada como morta.')
    'en'=@('Installation folder exists.','Installation folder does NOT exist.','Icon executable found: {0}','Icon executable not found: {0}','Uninstaller uses Windows Installer.','Uninstaller found: {0}','Uninstaller not found: {0}','Uses MsiExec.exe; the MSI entry will not be marked as orphaned.')
    'es'=@('La carpeta de instalación existe.','La carpeta de instalación NO existe.','Ejecutable del icono encontrado: {0}','Ejecutable del icono no encontrado: {0}','El desinstalador usa Windows Installer.','Desinstalador encontrado: {0}','Desinstalador no encontrado: {0}','Usa MsiExec.exe; la entrada MSI no se marcará como inactiva.')
    'fr'=@('Le dossier d’’installation existe.','Le dossier d’’installation n’’existe PAS.','Exécutable de l’’icône trouvé : {0}','Exécutable de l’’icône introuvable : {0}','Le désinstalleur utilise Windows Installer.','Désinstalleur trouvé : {0}','Désinstalleur introuvable : {0}','Utilise MsiExec.exe ; l’’entrée MSI ne sera pas marquée comme orpheline.')
    'de'=@('Installationsordner ist vorhanden.','Installationsordner ist NICHT vorhanden.','Icon-Programmdatei gefunden: {0}','Icon-Programmdatei nicht gefunden: {0}','Deinstallationsprogramm verwendet Windows Installer.','Deinstallationsprogramm gefunden: {0}','Deinstallationsprogramm nicht gefunden: {0}','Verwendet MsiExec.exe; der MSI-Eintrag wird nicht als verwaist markiert.')
    'it'=@('La cartella di installazione esiste.','La cartella di installazione NON esiste.','Eseguibile dell’’icona trovato: {0}','Eseguibile dell’’icona non trovato: {0}','Il programma di disinstallazione usa Windows Installer.','Programma di disinstallazione trovato: {0}','Programma di disinstallazione non trovato: {0}','Usa MsiExec.exe; la voce MSI non verrà segnalata come orfana.')
    'ja'=@('インストールフォルダーが存在します。','インストールフォルダーが存在しません。','アイコンの実行ファイルが見つかりました: {0}','アイコンの実行ファイルが見つかりません: {0}','アンインストーラーは Windows Installer を使用します。','アンインストーラーが見つかりました: {0}','アンインストーラーが見つかりません: {0}','MsiExec.exe を使用しています。MSI 項目は孤立として扱いません。')
    'ko'=@('설치 폴더가 있습니다.','설치 폴더가 없습니다.','아이콘 실행 파일을 찾았습니다: {0}','아이콘 실행 파일을 찾을 수 없습니다: {0}','제거 프로그램이 Windows Installer를 사용합니다.','제거 프로그램을 찾았습니다: {0}','제거 프로그램을 찾을 수 없습니다: {0}','MsiExec.exe를 사용합니다. MSI 항목은 고아로 표시하지 않습니다.')
    'zh-CN'=@('安装文件夹存在。','安装文件夹不存在。','找到图标可执行文件：{0}','未找到图标可执行文件：{0}','卸载程序使用 Windows Installer。','找到卸载程序：{0}','未找到卸载程序：{0}','使用 MsiExec.exe；不会将 MSI 条目标记为孤立。')
    'ru'=@('Папка установки существует.','Папка установки НЕ существует.','Исполняемый файл значка найден: {0}','Исполняемый файл значка не найден: {0}','Деинсталлятор использует Windows Installer.','Деинсталлятор найден: {0}','Деинсталлятор не найден: {0}','Используется MsiExec.exe; запись MSI не будет отмечена как осиротевшая.')
}

# Auto-elevação para Administrador se necessário
if (-not ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Write-Host $script:Action[0] -ForegroundColor Yellow
    Start-Process powershell -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`"" -Verb RunAs
    exit
}

Show-AppSessionMetadata -Version '1.0.0'

$RegistryPaths = @(
    @{ Path = "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\*"; Name = "HKLM 64-bit"; Hive = "HKEY_LOCAL_MACHINE"; KeyPrefix = "SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall" },
    @{ Path = "HKLM:\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\*"; Name = "HKLM 32-bit"; Hive = "HKEY_LOCAL_MACHINE"; KeyPrefix = "SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall" },
    @{ Path = "HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\*"; Name = "HKCU"; Hive = "HKEY_CURRENT_USER"; KeyPrefix = "SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall" }
)

$WindowsInstallers = @("msiexec.exe", "msiexec")

function Expand-MyPath ([string]$path) {
    if ([string]::IsNullOrWhiteSpace($path)) { return $null }
    $clean = $path.Trim().Trim('"')
    return [System.Environment]::ExpandEnvironmentVariables($clean)
}

function Extract-Executable ([string]$cmd) {
    if ([string]::IsNullOrWhiteSpace($cmd)) { return $null }
    $cmd = $cmd.Trim()
    
    if ($cmd.StartsWith('"')) {
        $end = $cmd.IndexOf('"', 1)
        if ($end -gt 0) {
            return Expand-MyPath ($cmd.Substring(1, $end - 1))
        }
    }
    
    if ($cmd -match '(?i)([a-zA-Z]:\\.*?\.(?:exe|com|bat|cmd|msi))(?=\s|$)') {
        return Expand-MyPath $matches[1]
    }
    
    $first = ($cmd -split '\s+')[0]
    return Expand-MyPath $first
}

function Extract-IconPath ([string]$icon) {
    if ([string]::IsNullOrWhiteSpace($icon)) { return $null }
    $clean = $icon.Trim() -replace ',-?\d+\s*$', ''
    return Expand-MyPath $clean
}

function Scan-Registry {
    $results = @()
    
    foreach ($reg in $RegistryPaths) {
        if (Test-Path $reg.Path) {
            $items = Get-ItemProperty -Path $reg.Path -ErrorAction SilentlyContinue
            foreach ($item in $items) {
                if (-not $item.DisplayName) { continue }
                
                $keyName = Split-Path $item.PSPath -Leaf
                $installLoc = Expand-MyPath $item.InstallLocation
                $uninstallStr = $item.UninstallString
                $quietUninstallStr = $item.QuietUninstallString
                $displayIcon = $item.DisplayIcon
                
                $evidence = @()
                $status = "SUSPEITO"
                $reason = $script:AnalysisReasons[$script:AppLanguage][5]
                
                # 1. InstallLocation
                if ($installLoc) {
                    if (Test-Path $installLoc) {
                        $status = "OK"
                        $reason = $script:AnalysisReasons[$script:AppLanguage][0]
                        $evidence += $script:EvidenceText[$script:AppLanguage][0]
                    } else {
                        $evidence += $script:EvidenceText[$script:AppLanguage][1]
                    }
                }
                
                # 2. DisplayIcon (se ainda não OK)
                if ($status -ne "OK") {
                    $iconPath = Extract-IconPath $displayIcon
                    if ($iconPath) {
                        if (Test-Path $iconPath -PathType Leaf) {
                            $status = "OK"
                            $reason = $script:AnalysisReasons[$script:AppLanguage][1]
                            $evidence += ($script:EvidenceText[$script:AppLanguage][2] -f $iconPath)
                        } else {
                            $evidence += ($script:EvidenceText[$script:AppLanguage][3] -f $iconPath)
                        }
                    }
                }
                
                # 3. QuietUninstall (se ainda não OK)
                if ($status -ne "OK") {
                    $quietExe = Extract-Executable $quietUninstallStr
                    if ($quietExe) {
                        $exeName = [System.IO.Path]::GetFileName($quietExe).ToLower()
                        if ($WindowsInstallers -contains $exeName) {
                            $evidence += $script:EvidenceText[$script:AppLanguage][4]
                        } elseif (Test-Path $quietExe -PathType Leaf) {
                            $status = "OK"
                            $reason = $script:AnalysisReasons[$script:AppLanguage][2]
                            $evidence += ($script:EvidenceText[$script:AppLanguage][5] -f $quietExe)
                        } else {
                            $evidence += ($script:EvidenceText[$script:AppLanguage][6] -f $quietExe)
                        }
                    }
                }
                
                # 4. UninstallString (se ainda não OK)
                if ($status -ne "OK") {
                    $uninstExe = Extract-Executable $uninstallStr
                    if ($uninstExe) {
                        $exeName = [System.IO.Path]::GetFileName($uninstExe).ToLower()
                        if ($WindowsInstallers -contains $exeName) {
                            $status = "SUSPEITO"
                            $reason = $script:AnalysisReasons[$script:AppLanguage][3]
                            $evidence += $script:EvidenceText[$script:AppLanguage][7]
                        } elseif (Test-Path $uninstExe -PathType Leaf) {
                            $status = "OK"
                            $reason = $script:AnalysisReasons[$script:AppLanguage][2]
                            $evidence += ($script:EvidenceText[$script:AppLanguage][5] -f $uninstExe)
                        } else {
                            $evidence += ($script:EvidenceText[$script:AppLanguage][6] -f $uninstExe)
                        }
                    }
                }
                
                # 5. Validação final de MORTO
                if ($installLoc -and -not (Test-Path $installLoc)) {
                    if ($uninstallStr -or $quietUninstallStr -or $displayIcon) {
                        if ($reason -notlike "*MSI*") {
                            $status = "MORTO"
                            $reason = $script:AnalysisReasons[$script:AppLanguage][4]
                        }
                    }
                }
                
                $results += [PSCustomObject]@{
                    Name             = [string]$item.DisplayName
                    RootName         = $reg.Name
                    Hive             = $reg.Hive
                    KeyPrefix        = $reg.KeyPrefix
                    Key              = $keyName
                    PSPath           = $item.PSPath
                    InstallLocation  = $installLoc
                    UninstallString  = $uninstallStr
                    Status           = $status
                    Reason           = $reason
                    Evidence         = $evidence
                }
            }
        }
    }
    return $results
}

function Backup-DeadApps ($deadApps) {
    if (-not $deadApps -or $deadApps.Count -eq 0) { return $false }
    $backupDir = Join-Path $env:LOCALAPPDATA 'Emertels\ClearDeath\Backups'
    if (-not (Test-Path -LiteralPath $backupDir)) { New-Item -ItemType Directory -Path $backupDir -Force | Out-Null }
    $timestamp = Get-Date -Format 'yyyyMMdd_HHmmss'
    $backupFile = Join-Path $backupDir "backup_apps_$timestamp.reg"
    $registryLines = New-Object 'System.Collections.Generic.List[string]'
    [void]$registryLines.Add('Windows Registry Editor Version 5.00')
    [void]$registryLines.Add('')
    Write-Host ("`n" + $script:Action[1]) -ForegroundColor Cyan
    $index = 0
    foreach ($app in $deadApps) {
        $index++
        $regPath = "$($app.Hive)\$($app.KeyPrefix)\$($app.Key)"
        $tempFile = "$backupFile.$index.tmp"
        & reg.exe export $regPath $tempFile /y 2>$null | Out-Null
        if ($LASTEXITCODE -ne 0 -or -not (Test-Path -LiteralPath $tempFile)) {
            Remove-Item -LiteralPath $tempFile,$backupFile -Force -ErrorAction SilentlyContinue
            Write-Host $script:Action[2] -ForegroundColor Red
            return $false
        }
        try {
            $content = Get-Content -LiteralPath $tempFile -Encoding Unicode -ErrorAction Stop | Where-Object { $_ -ne 'Windows Registry Editor Version 5.00' }
            foreach ($line in $content) { [void]$registryLines.Add([string]$line) }
            Remove-Item -LiteralPath $tempFile -Force -ErrorAction Stop
        } catch {
            Remove-Item -LiteralPath $tempFile,$backupFile -Force -ErrorAction SilentlyContinue
            Write-Host $script:Action[3] -ForegroundColor Red
            return $false
        }
    }
    try { [System.IO.File]::WriteAllLines($backupFile, $registryLines.ToArray(), [System.Text.Encoding]::Unicode) }
    catch {
        Remove-Item -LiteralPath $backupFile -Force -ErrorAction SilentlyContinue
        Write-Host $script:Action[4] -ForegroundColor Red
        return $false
    }
    Write-Host ($script:Action[5] -f $backupFile) -ForegroundColor Green
    return $true
}
function Log-Removal ($app) {
    $logDir = Join-Path $env:LOCALAPPDATA 'Emertels\ClearDeath'
    if (-not (Test-Path -LiteralPath $logDir)) { New-Item -ItemType Directory -Path $logDir -Force | Out-Null }
    $logFile = Join-Path $logDir 'removals.log'
    $timestamp = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'
    $entry = "$timestamp - Removed: $($app.Name) ($($app.Key))`n    Install path: $($app.InstallLocation)`n    Registry: $($app.RootName)`n"
    Add-Content -LiteralPath $logFile -Value $entry -Encoding UTF8 -ErrorAction SilentlyContinue
}
function Remove-SelectedApps ($appsToRemove) {
    if (-not $appsToRemove -or $appsToRemove.Count -eq 0) {
        Write-Host ("`n" + $script:Action[6])
        return
    }
    
    Write-Host "`n==============================================================================" -ForegroundColor Red
    Write-Host $script:Action[7] -ForegroundColor Red
    Write-Host "==============================================================================" -ForegroundColor Red
    
    foreach ($app in $appsToRemove) {
        Write-Host "- $($app.Name)" -ForegroundColor Red
    }
    
    Write-Host ("`n" + $script:Action[8]) -ForegroundColor Yellow
    Write-Host ($script:Action[9] + "`n")
    
    $confirm = Read-Host ($script:Action[10] -f $script:ConfirmToken)
    if ($confirm -ne $script:ConfirmToken) {
        Write-Host ("`n" + $script:Action[11]) -ForegroundColor Yellow
        return
    }
    
    if (-not (Backup-DeadApps $appsToRemove)) {
        Write-Host $script:Action[12] -ForegroundColor Red
        return
    }
    
    Write-Host ("`n" + $script:Action[13]) -ForegroundColor Cyan
    $success = 0
    
    foreach ($app in $appsToRemove) {
        Write-Host ($script:Action[14] -f $app.Name)
        
        try {
            Remove-Item -LiteralPath $app.PSPath -Recurse -Force -ErrorAction Stop
            Log-Removal $app
            Write-Host ("    " + $script:Action[15]) -ForegroundColor Green
            $success++
        } catch {
            Write-Host ("    " + ($script:Action[16] -f $_)) -ForegroundColor Red
        }
    }
    
    Write-Host ("`n" + ($script:Action[17] -f $success,$appsToRemove.Count)) -ForegroundColor Green
}

# MAIN EXECUTION
Write-Host "==============================================================================" -ForegroundColor White
Write-Host ("       " + $script:Action[18]) -ForegroundColor White
Write-Host "==============================================================================" -ForegroundColor White
Write-Host ("`n" + $script:Action[19]) -ForegroundColor Cyan

$allApps = Scan-Registry
$okApps = @($allApps | Where-Object { $_.Status -eq "OK" })
$deadApps = @($allApps | Where-Object { $_.Status -eq "MORTO" })
$suspiciousApps = @($allApps | Where-Object { $_.Status -eq "SUSPEITO" })

Write-Host "`n=============================================================================="
Write-Host ("             {0}" -f $script:Ui[7])
Write-Host "=============================================================================="
Write-Host ("{0} : {1}" -f $script:Ui[8],$allApps.Count)
Write-Host ("{0,-16}: {1}" -f "OK",$okApps.Count) -ForegroundColor Green
Write-Host ("{0,-16}: {1}" -f $script:Ui[9],$deadApps.Count) -ForegroundColor Red
Write-Host ("{0,-16}: {1}" -f $script:Ui[10],$suspiciousApps.Count) -ForegroundColor Yellow

if ($deadApps.Count -gt 0) {
    Write-Host ("`n{0}" -f $script:Ui[11]) -ForegroundColor Red
    Write-Host "------------------------------------------------------------------------------"
    $i = 1
    foreach ($app in $deadApps) {
        Write-Host "[$i] $($app.Name)" -ForegroundColor Red
        if ($app.InstallLocation) { Write-Host ("    {0}: {1}" -f $script:Action[20],$app.InstallLocation) }
        Write-Host ("    {0}: {1}" -f $script:Action[21],$app.RootName)
        Write-Host ("    {0}: {1}" -f $script:Action[22],$app.Key)
        Write-Host ("    {0}: {1}`n" -f $script:Action[23],$app.Reason)
        $i++
    }
} else {
    Write-Host ("`n{0}" -f $script:Ui[12]) -ForegroundColor Green
}

# MENU LOOP
while ($true) {
    Write-Host "`n=============================================================================="
    Write-Host $script:Ui[0]
    Write-Host "=============================================================================="
    Write-Host ("1 - {0}" -f $script:Ui[1])
    Write-Host ("2 - {0}" -f $script:Ui[2])
    Write-Host ("3 - {0}" -f $script:Ui[3])
    Write-Host ("4 - {0}" -f $script:Ui[4])
    Write-Host ("5 - {0}" -f $script:Ui[5])
    
    $choice = Read-Host ("`n{0}" -f $script:Ui[6])
    
    if ($choice -eq "1") {
        if ($deadApps.Count -gt 0) {
            $i = 1
            foreach ($app in $deadApps) {
                Write-Host "[$i] $($app.Name)" -ForegroundColor Red
                $i++
            }
        } else {
            Write-Host $script:Ui[14] -ForegroundColor Green
        }
    }
    elseif ($choice -eq "2") {
        if ($suspiciousApps.Count -gt 0) {
            Write-Host ("`n" + $script:Action[24]) -ForegroundColor Yellow
            $i = 1
            foreach ($app in $suspiciousApps) {
                Write-Host ("[$i] $($app.Name) - {0}: $($app.Reason)" -f $script:Action[23]) -ForegroundColor Yellow
                $i++
            }
        } else {
            Write-Host $script:Ui[13] -ForegroundColor Green
        }
    }
    elseif ($choice -eq "3") {
        if ($deadApps.Count -eq 0) {
            Write-Host $script:Ui[15] -ForegroundColor Green
            continue
        }
        Write-Host ("`n" + $script:Action[25])
        $inputSel = Read-Host $script:Ui[18]
        if ($inputSel -eq "ALL") {
            Remove-SelectedApps $deadApps
        } else {
            $nums = $inputSel -split ',' | ForEach-Object { $_.Trim() }
            $toRemove = @()
            foreach ($n in $nums) {
                [int]$idx = 0
                if ([int]::TryParse($n, [ref]$idx) -and $idx -ge 1 -and $idx -le $deadApps.Count) {
                    $toRemove += $deadApps[$idx - 1]
                }
            }
            Remove-SelectedApps $toRemove
        }
    }
    elseif ($choice -eq "4") {
        Remove-SelectedApps $deadApps
    }
    elseif ($choice -eq "5") {
        Write-Host $script:Ui[17]
        break
    }
    else {
        Write-Host $script:Ui[16] -ForegroundColor Yellow
    }
}













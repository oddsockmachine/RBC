(ns app.rpc
  (:require-macros
    [javelin.core :refer [defc defc=]])
  (:require
   [javelin.core]
   [castra.core :refer [mkremote]]))

(defc stateE nil)
(defc stateW {:random nil})
(defc stateR {:random nil})
(defc error nil)
(defc loading [])

(defc= random-number (get stateR :random))
(defc= ws-mdl (get stateW :random))
(defc= exclaim-c stateE)

(def get-state
  (mkremote 'app.api/get-state stateR error loading))

(def do-exclaim
  (mkremote 'app.api/exclaim stateE error loading))

(defc env-list nil)
(def get-env-list
  (mkremote 'app.api/get-env-list env-list error loading))


(defc nodule-list nil)
(def get-nodule-list
  (mkremote 'app.api/get-nodule-list nodule-list error loading))


; (def get-ws-mdl
;   (mkremote 'app.api/get-ws-mdl stateW error loading))

(defc ws-list nil)
(def get-ws-from-env
  (mkremote 'app.api/get-ws-from-env ws-list error loading))



(defn init []
  ; (get-state)
  (get-nodule-list))
  ; (get-ws-from-env "gaga"))
  ; (do-exclaim [])
  ; (js/setInterval get-ws-mdl 15000)
  ; (js/setInterval get-state 15000))

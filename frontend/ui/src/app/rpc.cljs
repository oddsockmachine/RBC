(ns app.rpc
  (:require-macros
    [javelin.core :refer [defc defc=]])
  (:require
   [javelin.core]
   [castra.core :refer [mkremote]]))

(defc error nil)
(defc loading [])



(defc nodule-list nil)
(def get-nodule-list
  (mkremote 'app.api/get-nodule-list nodule-list error loading))


(defc all-nodule-stats nil)
(def get-all-nodule-stats
  (mkremote 'app.api/all-nodule-stats all-nodule-stats error loading))




(defn init []
  ; (get-state)
  (get-all-nodule-stats)
  (get-nodule-list))
  ; (get-ws-from-env "gaga"))
  ; (do-exclaim [])
  ; (js/setInterval get-ws-mdl 15000)
  ; (js/setInterval get-state 15000))

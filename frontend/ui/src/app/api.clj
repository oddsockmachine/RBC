(ns app.api
  (:require [castra.core :refer [defrpc]])
  (:require [app.db :refer [get-all-ws-from-env env-to-sql-hostname]]))

(defrpc get-state []
  (let [num (rand-int 100)]
    (prn "get-state")
    (prn num)
    {:random num}))

; (defrpc get-ws-mdl []
;   (let [num (rand-int 1000)]
;         ; mydb (assoc dbspec :host "ec2us-mysql1-1-gaga.anaplan.com")]
;         ; data (get-ws-mdls mydb ["Finance" "Workflow POC"])]
;     (prn "get-ws-mdl")
;     ; (prn mydb)
;     ; (prn data)
;     {:random num}))

(defrpc exclaim [ws]
  (let [num (rand-int 1000)]
        ; mydb (assoc dbspec :host "ec2us-mysql1-1-gaga.anaplan.com")
        ; data (get-ws-mdls mydb [ws])]
    (prn "exclaim!!")
    ; (prn mydb)
    ; (prn data)
    "foo"))

(defrpc get-env-list []
  (let [envs ["gaga" "nurding" "kesha" "qa2" "kanye" "bieber" "drake" "chvrches" "gaga" "nurding" "kesha" "qa2"]]
    (prn envs)
    envs))


(defrpc get-ws-from-env [env]
  (let [num (rand-int 1000)
        sql-server (env-to-sql-hostname env)
        data (get-all-ws-from-env sql-server)]
    ; (prn data)
    data))




(defrpc get-nodule-list []
  ; (let [nodules {"abc123" "balcony" "def456" "living room" "ghi789" "kitchen" "jkl012" "bedroom"}])
  (let [nodules ["abc123" "def456" "ghi789" "jkl012"]]
  ; (let [nodules [{:uid "abc123" :name "balcony"} {:uid "def456" :name "living room"} {:uid "ghi789" :name "kitchen"} {:uid "jkl012" :name "bedroom"}]]
    (prn nodules)
    nodules))

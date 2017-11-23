(ns mq-test.core
  (:gen-class)
  (:require [clojurewerkz.machine-head.client :as mh]
            [clojure.string :as str]
            [clojure.data.json :as json]))

(defn handle-delivery
  [^String url _ ^bytes payload]
  (let [t (nth (str/split url #"/") 0)]
    (println (format "[consumer] received %s for topic %s" (String. payload "UTF-8") t))))

(def topics ["presence" "logs" "errors" "report" "sensors"])


(defn start-subscriber
  [conn ^String topic]
  (let [channel (str topic "/#")]
    (mh/subscribe conn
                {channel 1}
                handle-delivery)))

(defn presence_msg
  [connected name]
  (json/write-str {"presence" (if connected "Connected" "Disconnected") "node" name}))

(defn -main
  [& args]
  (let [name    "collector"
        conn  (mh/connect "tcp://127.0.0.1:1883" name)]
    (doseq [t topics]
      (mh/subscribe conn
                    {(str t "/#") 1}
                    handle-delivery))
    (mh/publish conn (str "presence/" name) (str (presence_msg true name)))
    ; (mh/subscribe conn {"americas/north/#" 1} handle-delivery)
    ; (mh/subscribe conn {"americas/south/#" 1} handle-delivery)
    ; (mh/subscribe conn {"americas/north/us/ca/+" 1} handle-delivery)
    ; ; (mh/subscribe conn {"#/tx/austin" 1} handle-delivery)
    ; (mh/subscribe conn {"europe/italy/rome" 1} handle-delivery)
    ; (mh/subscribe conn {"asia/southeast/hk/+" 1} handle-delivery)
    ; (mh/subscribe conn {"asia/southeast/#" 1} handle-delivery)
    ; (prn "subscribed")
    ; (mh/publish conn "americas/north/us/ca/sandiego"     "San Diego update")
    ; (mh/publish conn "americas/north/us/ca/berkeley"     "Berkeley update")
    ; (mh/publish conn "americas/north/us/ca/sanfrancisco" "SF update")
    ; (mh/publish conn "americas/north/us/ny/newyork"      "NYC update")
    ; (mh/publish conn "americas/south/brazil/saopaolo"    "São Paolo update")
    ; (mh/publish conn "asia/southeast/hk/hongkong"        "Hong Kong update")
    ; (mh/publish conn "asia/southeast/japan/kyoto"        "Kyoto update")
    ; (mh/publish conn "asia/southeast/prc/shanghai"       "Shanghai update")
    ; (mh/publish conn "europe/italy/roma"                 "Rome update")
    ; (mh/publish conn "europe/france/paris"               "Paris update")
    ; (mh/publish conn "report/foo"               "sensor update")
    ; (mh/publish conn "presence/foo"               "presence update")
    (prn "sent")
    (Thread/sleep 15000)
    (prn "disconnecting")
    (mh/disconnect conn)
    ; (prn (presence_msg true name))
    ; (prn (presence_msg false name))
    (System/exit 0)))

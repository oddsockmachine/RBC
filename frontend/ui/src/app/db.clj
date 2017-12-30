(ns app.db
  (:require [castra.core :refer [defrpc]]))

(require '[clojure.java.jdbc :as j])
(require '[honeysql.core :as sql])
         ; '[honeysql.helpers :refer :all :as helpers])



(def dbspec {:dbtype "mysql"
             :user "apcustomer"
             :dbname "apcustomer"
             :password "apcustomer"
             :port 3306
             :host "ec2us-mysql1-1-gaga.anaplan.com"})

(defn connect-db
  [host password]
  (assoc dbspec :host host :password password))

(def sql-ws-all {:select [:name]
                 :from [:workspace]})

(def sql-ws-mdl-all {:select [[:workspace.name "ws"] [:model.name "mdl"]]
                     :from [:model]
                     :join [:workspace [:= :workspace.workspaceGuid :model.currentWorkspaceGuid]]})

(defn sql-ws-query
  [ws-names]
  (if (= (count ws-names) 0)  ; if no names specified
      sql-ws-mdl-all  ; use default query
      (assoc sql-ws-mdl-all :where [:in :workspace.name ws-names]))) ; else add where clause to query

(defn consolidate [ms]
  (apply merge-with conj (zipmap (mapcat keys ms) (repeat [])) ms))

(defn extract-values [data]
  (apply hash-map (vals data)))

(defn get-ws-mdls
  [db-conn ws-names]
  (let [quer (sql-ws-query ws-names)]
    (prn (sql/format quer))  ; debug
    (consolidate (map extract-values (into [] (j/query db-conn (sql/format quer)))))))

(defn env-to-sql-hostname
  [env]
  (str "ec2us-mysql1-1-" env ".anaplan.com"))

(defn get-all-ws-from-env
  [host]
  (let [db-conn (connect-db host "apcustomer")
        data (j/query db-conn (sql/format sql-ws-all))]
    (prn host)
    (into [] (map #(:name %1) data))))

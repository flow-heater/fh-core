pub(crate) mod filters {
    use crate::server::with_sender;
    use fh_core::ReqSender;
    use fh_db::ReqCmd;
    use uuid::Uuid;
    use warp::Filter;

    pub(crate) fn admin_filters(
        tx: ReqSender<ReqCmd>,
    ) -> impl Filter<Extract = impl warp::Reply, Error = warp::Rejection> + Clone {
        create_processor(tx.clone())
            .or(get_processor(tx.clone()))
            .or(update_processor(tx.clone()))
            .or(delete_processor(tx))
    }

    pub(crate) fn create_processor(
        tx: ReqSender<ReqCmd>,
    ) -> impl Filter<Extract = impl warp::Reply, Error = warp::Rejection> + Clone {
        warp::path!("admin" / "processor")
            .and(with_sender(tx))
            .and(warp::post())
            .and(warp::body::json())
            .and_then(super::handlers::create_processor)
    }

    pub(crate) fn get_processor(
        tx: ReqSender<ReqCmd>,
    ) -> impl Filter<Extract = impl warp::Reply, Error = warp::Rejection> + Clone {
        warp::path!("admin" / "processor" / Uuid)
            .and(with_sender(tx))
            .and(warp::get())
            .and_then(super::handlers::get_processor)
    }

    pub(crate) fn update_processor(
        tx: ReqSender<ReqCmd>,
    ) -> impl Filter<Extract = impl warp::Reply, Error = warp::Rejection> + Clone {
        warp::path!("admin" / "processor" / Uuid)
            .and(with_sender(tx))
            .and(warp::put())
            .and(warp::body::json())
            .and_then(super::handlers::update_processor)
    }

    pub(crate) fn delete_processor(
        tx: ReqSender<ReqCmd>,
    ) -> impl Filter<Extract = impl warp::Reply, Error = warp::Rejection> + Clone {
        warp::path!("admin" / "processor" / Uuid)
            .and(with_sender(tx))
            .and(warp::delete())
            .and_then(super::handlers::delete_processor)
    }
}

pub(crate) mod handlers {
    use crate::server::FhHttpError;
    use fh_core::{FhLockingError, ReqSender};
    use fh_db::{request_processor::RequestProcessor, ReqCmd};
    use tokio::sync::oneshot;
    use uuid::Uuid;

    pub(crate) async fn create_processor(
        tx: ReqSender<ReqCmd>,
        processor: RequestProcessor,
    ) -> Result<impl warp::Reply, warp::Rejection> {
        let mut tx2 = tx
            .lock()
            .map_err(|e| warp::reject::custom(FhLockingError::new(e.to_string())))?
            .clone();

        let (resp_tx, resp_rx) = oneshot::channel();
        tx2.send(ReqCmd::CreateRequestProcessor {
            proc: processor.clone(),
            cmd_tx: resp_tx,
        })
        .await
        .map_err(|e| warp::reject::custom(FhHttpError::new(e)))?;

        let res = resp_rx
            .await
            .map_err(|e| warp::reject::custom(FhHttpError::new(e)))?
            .map_err(|e| warp::reject::custom(FhHttpError::new(e)))?;

        Ok(warp::reply::json(&res))
    }

    pub(crate) async fn get_processor(
        id: Uuid,
        tx: ReqSender<ReqCmd>,
    ) -> Result<impl warp::Reply, warp::Rejection> {
        let mut tx2 = tx
            .lock()
            .map_err(|e| warp::reject::custom(FhLockingError::new(e.to_string())))?
            .clone();

        let (resp_tx, resp_rx) = oneshot::channel();
        tx2.send(ReqCmd::GetRequestProcessor {
            id,
            cmd_tx: resp_tx,
        })
        .await
        .map_err(|e| warp::reject::custom(FhHttpError::new(e)))?;

        let proc = resp_rx
            .await
            .map_err(|e| warp::reject::custom(FhHttpError::new(e)))?
            .map_err(|e| warp::reject::custom(FhHttpError::new(e)))?;

        Ok(warp::reply::json(&proc))
    }

    pub(crate) async fn update_processor(
        id: Uuid,
        tx: ReqSender<ReqCmd>,
        processor: RequestProcessor,
    ) -> Result<impl warp::Reply, warp::Rejection> {
        let mut tx2 = tx
            .lock()
            .map_err(|e| warp::reject::custom(FhLockingError::new(e.to_string())))?
            .clone();

        let (resp_tx, resp_rx) = oneshot::channel();
        tx2.send(ReqCmd::UpdateRequestProcessor {
            id,
            proc: processor.clone(),
            cmd_tx: resp_tx,
        })
        .await
        .map_err(|e| warp::reject::custom(FhHttpError::new(e)))?;

        let res = resp_rx
            .await
            .map_err(|e| warp::reject::custom(FhHttpError::new(e)))?
            .map_err(|e| warp::reject::custom(FhHttpError::new(e)))?;

        Ok(warp::reply::json(&res))
    }

    pub(crate) async fn delete_processor(
        id: Uuid,
        tx: ReqSender<ReqCmd>,
    ) -> Result<impl warp::Reply, warp::Rejection> {
        let mut tx2 = tx
            .lock()
            .map_err(|e| warp::reject::custom(FhLockingError::new(e.to_string())))?
            .clone();

        let (resp_tx, resp_rx) = oneshot::channel();
        tx2.send(ReqCmd::DeleteRequestProcessor {
            id,
            cmd_tx: resp_tx,
        })
        .await
        .map_err(|e| warp::reject::custom(FhHttpError::new(e)))?;

        let _res = resp_rx
            .await
            .map_err(|e| warp::reject::custom(FhHttpError::new(e)))?
            .map_err(|e| warp::reject::custom(FhHttpError::new(e)))?;

        Ok(warp::reply())
    }
}

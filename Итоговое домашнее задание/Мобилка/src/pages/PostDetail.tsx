import { IonPage, IonHeader, IonToolbar, IonTitle, IonContent, IonButtons, IonBackButton, IonCard, IonCardHeader, IonCardTitle, IonCardContent } from '@ionic/react';
import { useEffect, useState } from 'react';
import { useParams } from 'react-router';
import { fetchPost } from '../services/api';
import LoadingSpinner from '../components/LoadingSpinner';

const PostDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [post, setPost] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadPost = async () => {
      try {
        setLoading(true);
        const data = await fetchPost(id);
        setPost(data);
        setError(null);
      } catch (err) {
        setError('Failed to load post. Please try again later.');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    loadPost();
  }, [id]);

  return (
    <IonPage>
      <IonHeader>
        <IonToolbar>
          <IonButtons slot="start">
            <IonBackButton defaultHref="/" />
          </IonButtons>
          <IonTitle>Post Details</IonTitle>
        </IonToolbar>
      </IonHeader>
      <IonContent>
        {loading && <LoadingSpinner />}

        {error && (
          <div className="ion-padding ion-text-center">
            <p>{error}</p>
          </div>
        )}

        {!loading && post && (
          <IonCard>
            <IonCardHeader>
              <IonCardTitle>{post.title}</IonCardTitle>
            </IonCardHeader>
            <IonCardContent>
              <p>{post.body}</p>
            </IonCardContent>
          </IonCard>
        )}
      </IonContent>
    </IonPage>
  );
};

export default PostDetail;
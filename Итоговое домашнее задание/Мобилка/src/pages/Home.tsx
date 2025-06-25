import { IonPage, IonHeader, IonToolbar, IonTitle, IonContent, IonList, IonRefresher, IonRefresherContent, RefresherEventDetail } from '@ionic/react';
import { useEffect, useState } from 'react';
import { fetchPosts } from '../services/api';
import PostCard from '../components/PostCard';
import LoadingSpinner from '../components/LoadingSpinner';

const Home: React.FC = () => {
  const [posts, setPosts] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadPosts();
  }, []);

  const loadPosts = async () => {
    try {
      setLoading(true);
      const data = await fetchPosts();
      setPosts(data);
      setError(null);
    } catch (err) {
      setError('Failed to load posts. Please try again later.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleRefresh = async (event: CustomEvent<RefresherEventDetail>) => {
    await loadPosts();
    event.detail.complete();
  };

  return (
    <IonPage>
      <IonHeader>
        <IonToolbar>
          <IonTitle>Blog Posts</IonTitle>
        </IonToolbar>
      </IonHeader>
      <IonContent fullscreen>
        <IonRefresher slot="fixed" onIonRefresh={handleRefresh}>
          <IonRefresherContent></IonRefresherContent>
        </IonRefresher>

        {loading && <LoadingSpinner />}

        {error && (
          <div className="ion-padding ion-text-center">
            <p>{error}</p>
          </div>
        )}

        {!loading && !error && (
          <IonList>
            {posts.map((post) => (
              <PostCard key={post.id} post={post} />
            ))}
          </IonList>
        )}
      </IonContent>
    </IonPage>
  );
};

export default Home;
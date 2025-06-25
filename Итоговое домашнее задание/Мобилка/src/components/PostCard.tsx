import { IonCard, IonCardHeader, IonCardTitle, IonCardContent, IonButton } from '@ionic/react';
import { useHistory } from 'react-router';

interface PostCardProps {
  post: {
    id: number;
    title: string;
    body: string;
  };
}

const PostCard: React.FC<PostCardProps> = ({ post }) => {
  const history = useHistory();

  const handleViewDetails = () => {
    history.push(`/post/${post.id}`);
  };

  return (
    <IonCard>
      <IonCardHeader>
        <IonCardTitle>{post.title}</IonCardTitle>
      </IonCardHeader>
      <IonCardContent>
        <p>{post.body.substring(0, 100)}...</p>
        <IonButton expand="block" onClick={handleViewDetails}>
          View Details
        </IonButton>
      </IonCardContent>
    </IonCard>
  );
};

export default PostCard;
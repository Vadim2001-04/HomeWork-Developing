import { IonSpinner } from '@ionic/react';

const LoadingSpinner: React.FC = () => {
  return (
    <div className="ion-text-center ion-padding">
      <IonSpinner name="crescent" />
      <p>Loading...</p>
    </div>
  );
};

export default LoadingSpinner;
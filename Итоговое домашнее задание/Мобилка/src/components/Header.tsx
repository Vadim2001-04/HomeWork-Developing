import { IonHeader, IonToolbar, IonTitle, IonButtons, IonBackButton, IonButton } from '@ionic/react';
import { useHistory } from 'react-router';

interface HeaderProps {
  title: string;
  showBackButton?: boolean;
  additionalButtons?: {
    text: string;
    handler: () => void;
  }[];
}

const Header: React.FC<HeaderProps> = ({ title, showBackButton = false, additionalButtons }) => {
  const history = useHistory();

  const handleBack = () => {
    history.goBack();
  };

  return (
    <IonHeader>
      <IonToolbar>
        {showBackButton && (
          <IonButtons slot="start">
            <IonBackButton defaultHref="/" onClick={handleBack} />
          </IonButtons>
        )}

        <IonTitle>{title}</IonTitle>

        {additionalButtons && (
          <IonButtons slot="end">
            {additionalButtons.map((button, index) => (
              <IonButton key={index} onClick={button.handler}>
                {button.text}
              </IonButton>
            ))}
          </IonButtons>
        )}
      </IonToolbar>
    </IonHeader>
  );
};

export default Header;